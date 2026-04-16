from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib import messages
from django.db.models import Q, Count
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from .models import Post, Category, Tag
from .forms import CommentForm


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
        return (
            Post.objects.filter(
                status='published',
                created_on__year=y,
                created_on__month=m,
            )
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
    archive_dates = Post.objects.filter(status='published').dates('created_on', 'month', order='DESC')
    return render(request, 'blog/archive.html', {'archive_dates': archive_dates})
