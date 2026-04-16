from datetime import date
from types import SimpleNamespace

from django.conf import settings
from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.utils import timezone

from .models import Post, Category, Tag
from .forms import CommentForm


def _post_local_year_month(row):
    """
    与归档索引一致：优先 created_on，否则 updated_on；按当前时区得到 (年, 月)。
    不用 ORM 的 __year/__month：在 MySQL + USE_TZ 且未装时区表时，与 Python 侧 localtime 可能不一致。
    """
    dt = row.get('created_on') or row.get('updated_on')
    if dt is None:
        return None
    if settings.USE_TZ and timezone.is_aware(dt):
        dt = timezone.localtime(dt)
    return dt.year, dt.month


class PostList(generic.ListView):
    queryset = Post.objects.filter(status='published').select_related(
        'category', 'author',
    ).prefetch_related('tags')
    template_name = 'blog/index.html'
    paginate_by = 5
    context_object_name = 'posts'


class CategoryView(generic.ListView):
    template_name = 'blog/category.html'
    paginate_by = 5
    context_object_name = 'posts'

    def get_queryset(self):
        self.category = get_object_or_404(Category, name=self.kwargs['category'])
        return (
            Post.objects.filter(category=self.category, status='published')
            .select_related('author', 'category')
            .prefetch_related('tags')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        return context


class CategoryListView(generic.TemplateView):
    template_name = 'blog/category_list.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories_with_count'] = (
            Category.objects.annotate(
                published_count=Count('posts', filter=Q(posts__status='published')),
            ).order_by('name')
        )
        return context


class TagView(generic.ListView):
    template_name = 'blog/tag.html'
    paginate_by = 5
    context_object_name = 'posts'

    def get_queryset(self):
        self.tag = get_object_or_404(Tag, slug=self.kwargs['slug'])
        return (
            Post.objects.filter(tags=self.tag, status='published')
            .select_related('author', 'category')
            .prefetch_related('tags')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['tag'] = self.tag
        return context


class ArchiveMonthView(generic.ListView):
    template_name = 'blog/archive_month.html'
    paginate_by = 5
    context_object_name = 'posts'

    def get_queryset(self):
        y = int(self.kwargs['year'])
        m = int(self.kwargs['month'])
        ids = []
        for row in (
            Post.objects.filter(status='published')
            .order_by('-created_on')
            .values('pk', 'created_on', 'updated_on')
        ):
            ym = _post_local_year_month(row)
            if ym == (y, m):
                ids.append(row['pk'])
        return (
            Post.objects.filter(pk__in=ids)
            .select_related('author', 'category')
            .prefetch_related('tags')
            .order_by('-created_on')
        )

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['archive_year'] = int(self.kwargs['year'])
        context['archive_month'] = int(self.kwargs['month'])
        return context


def post_detail(request, slug):
    post = get_object_or_404(
        Post.objects.select_related('category', 'author').prefetch_related('tags'),
        slug=slug,
        status='published',
    )
    comments = post.comments.filter(active=True)
    new_comment = None

    next_post = Post.objects.filter(status='published', created_on__lt=post.created_on).order_by('-created_on').first()
    prev_post = Post.objects.filter(status='published', created_on__gt=post.created_on).order_by('created_on').first()

    related_posts = list(
        Post.objects.filter(category=post.category, status='published')
        .exclude(pk=post.pk)
        .select_related('author')
        .order_by('-created_on')[:5]
    )

    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.active = False
            new_comment.save()
            messages.success(
                request,
                '评论已提交，管理员审核通过后将公开展示。感谢您的参与！',
            )
            return redirect('post_detail', slug=post.slug)
    else:
        comment_form = CommentForm()

    return render(
        request,
        'blog/post_detail.html',
        {
            'post': post,
            'comments': comments,
            'comment_form': comment_form,
            'new_comment': new_comment,
            'next_post': next_post,
            'prev_post': prev_post,
            'related_posts': related_posts,
        },
    )


def search_posts(request):
    query = (request.GET.get('q') or '').strip()
    search_results = Post.objects.none()

    if query:
        search_results = Post.objects.filter(
            Q(title__icontains=query)
            | Q(content__icontains=query)
            | Q(excerpt__icontains=query),
            status='published',
        ).select_related('author', 'category').prefetch_related('tags').order_by('-created_on')

    paginator = Paginator(search_results, 5)
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(
        request,
        'blog/search.html',
        {
            'query': query,
            'search_results': page_obj.object_list,
            'page_obj': page_obj,
            'is_paginated': page_obj.has_other_pages(),
            'paginator': paginator,
        },
    )


def about(request):
    return render(request, 'blog/about.html')


def archive_index(request):
    # 不在 SQL 里用 TruncMonth/dates：MySQL 未加载时区表时 CONVERT_TZ 会报错。在 Python 里按当前时区聚合成 (年, 月)。
    # created_on 在个别库/导入数据下可能读成 None，用 updated_on 兜底；模板里用 SimpleNamespace，避免 dict 在 {% url %} 中解析异常。
    month_keys = {}
    for row in (
        Post.objects.filter(status='published')
        .order_by('-created_on')
        .values('created_on', 'updated_on')
    ):
        ym = _post_local_year_month(row)
        if ym is None:
            continue
        key = (ym[0], ym[1])
        if key not in month_keys:
            month_keys[key] = date(ym[0], ym[1], 1)
    months = [
        SimpleNamespace(year=y, month=mo, label=month_keys[(y, mo)])
        for (y, mo) in sorted(month_keys.keys(), reverse=True)
    ]
    return render(request, 'blog/archive.html', {'archive_months': months})
