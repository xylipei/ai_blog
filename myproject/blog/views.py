from django.shortcuts import render, get_object_or_404, redirect
from django.views import generic
from django.contrib import messages
from .models import Post, Category, Comment
from .forms import CommentForm
from django.db.models import Q
from django.http import JsonResponse, StreamingHttpResponse
import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI
from langchain.schema import HumanMessage
import json

# Load environment variables
load_dotenv(dotenv_path=os.path.join(os.path.dirname(os.path.dirname(os.path.dirname(__file__))), '.env'))

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

import os
import json
from django.http import JsonResponse
from langchain.chains import LLMChain
from langchain.prompts import PromptTemplate
from typing import Any, List, Mapping, Optional

def chat_with_ai(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            user_message = data.get('message')
            user_id = data.get('userid', 'default_user')
            print(f"Received message: {user_message}, User ID: {user_id}")
            if not user_message:
                return JsonResponse({'error': 'No message provided'}, status=400)

            openai_api_key = os.getenv("OPENAI_API_KEY")
            if not openai_api_key or openai_api_key == "YOUR_OPENAI_API_KEY":
                return JsonResponse({'reply': '抱歉，我的大脑（OpenAI API Key）还没配置好，暂时无法回复。请联系管理员设置OpenAI API Key。'})

            chat_model = ChatOpenAI(
                api_key=openai_api_key,
                model="deepseek-chat",
                temperature=0.7,
                streaming=True  # 启用流式输出
            )

            # 定义提示词模板
            prompt_template = """你是一个专业的博客助手，你的名字为：可乐不加冰，请用中文回答用户的问题。
            回答要求：
            - 保持专业但友好的语气
            - 回答简洁明了，不超过200字
            - 如果问题与博客内容相关，优先参考博客文章回答
            - 避免提供医疗、法律等专业建议
            
            用户问题：{user_input}"""
            
            # 定义流式响应生成器
            def stream_response_generator():
                try:
                    formatted_prompt = prompt_template.format(user_input=user_message)
                    for chunk in chat_model.stream([HumanMessage(content=formatted_prompt)]):
                        if chunk.content:
                            yield chunk.content
                except Exception as e:
                    print(f"Error during streaming: {e}")
                    yield f"Error: {str(e)}"

            # 返回 StreamingHttpResponse
            response = StreamingHttpResponse(stream_response_generator(), content_type='text/plain')
            return response

        except Exception as e:
            print(f"Error processing request: {e}")
            return JsonResponse({'error': str(e)}, status=500)
    return JsonResponse({'error': 'Only POST method is allowed'}, status=405)
