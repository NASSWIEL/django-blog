from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Post
from .forms import PostForm
from django.contrib.auth.models import User
from django.http import HttpResponseForbidden
# Create your views here.


def home(request):
    posts = Post.objects.all().order_by('-date_posted')
    
    # Filter by category if specified
    category = request.GET.get('category')
    if category and category != 'all':
        posts = posts.filter(category=category)
    
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'posts': page_obj,
        'current_category': category
    }
    return render (request, 'blog/home.html',context)

def about(request) :
    return render (request, 'blog/about.html',{'title': 'About'})

@login_required
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            messages.success(request, 'Your post has been created!')
            return redirect('blog-home')
    else:
        form = PostForm()
    return render(request, 'blog/post_create.html', {'form': form})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    # Get related posts from the same author (excluding current post)
    author_posts = Post.objects.filter(author=post.author).exclude(pk=pk).order_by('-date_posted')[:3]
    # Get other recent posts (excluding current post and author's posts)
    related_posts = Post.objects.exclude(pk=pk).exclude(author=post.author).order_by('-date_posted')[:3]
    
    context = {
        'post': post,
        'author_posts': author_posts,
        'related_posts': related_posts,
    }
    return render(request, 'blog/post_detail.html', context)

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, 'Your post has been updated!')
            return redirect('post-detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form, 'post': post})

@login_required
def post_delete(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.user != post.author:
        return HttpResponseForbidden()
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Your post has been deleted!')
        return redirect('blog-home')
    return render(request, 'blog/post_confirm_delete.html', {'post': post})

def user_posts(request, username):
    user = get_object_or_404(User, username=username)
    posts = Post.objects.filter(author=user).order_by('-date_posted')
    return render(request, 'blog/user_posts.html', {'posts': posts, 'page_user': user})