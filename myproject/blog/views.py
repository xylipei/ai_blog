from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib import messages
from .models import Post, Category, Comment
from .forms import CommentForm
from django.db.models import Q

# Create your views here.

class PostList(generic.ListView):
    queryset = Post.objects.filter(status='published')
    template_name = 'blog/index.html'
    paginate_by = 5
    context_object_name = 'posts'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['categories'] = Category.objects.all()
        context['recent_posts'] = Post.objects.filter(status='published').order_by('-created_on')[:5]
        return context

class CategoryView(generic.ListView):
    template_name = 'blog/category.html'
    paginate_by = 5
    context_object_name = 'posts'

    def get_queryset(self):
        self.category = get_object_or_404(Category, name=self.kwargs['category'])
        return Post.objects.filter(category=self.category, status='published')
    
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['category'] = self.category
        context['categories'] = Category.objects.all()
        context['recent_posts'] = Post.objects.filter(status='published').order_by('-created_on')[:5]
        return context

def post_detail(request, slug):
    post = get_object_or_404(Post, slug=slug, status='published')
    comments = post.comments.filter(active=True)
    new_comment = None
    
    # 获取前一篇和后一篇文章
    next_post = Post.objects.filter(status='published', created_on__lt=post.created_on).order_by('-created_on').first()
    prev_post = Post.objects.filter(status='published', created_on__gt=post.created_on).order_by('created_on').first()
    
    if request.method == 'POST':
        comment_form = CommentForm(data=request.POST)
        if comment_form.is_valid():
            new_comment = comment_form.save(commit=False)
            new_comment.post = post
            new_comment.save()
            messages.success(request, '评论已提交，感谢您的参与！')
            return redirect('post_detail', slug=post.slug)
    else:
        comment_form = CommentForm()
    
    return render(request, 'blog/post_detail.html', {
        'post': post,
        'comments': comments,
        'comment_form': comment_form,
        'new_comment': new_comment,
        'categories': Category.objects.all(),
        'recent_posts': Post.objects.filter(status='published').order_by('-created_on')[:5],
        'next_post': next_post,
        'prev_post': prev_post
    })

def search_posts(request):
    query = request.GET.get('q')
    search_results = []
    
    if query:
        search_results = Post.objects.filter(
            Q(title__icontains=query) | 
            Q(content__icontains=query) |
            Q(excerpt__icontains=query),
            status='published'
        )
    
    return render(request, 'blog/search.html', {
        'query': query,
        'search_results': search_results,
        'categories': Category.objects.all(),
        'recent_posts': Post.objects.filter(status='published').order_by('-created_on')[:5]
    })
