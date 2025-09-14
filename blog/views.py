from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from .models import Post
from .forms import PostForm
# Create your views here.


def home(request):
    posts = Post.objects.all().order_by('-date_posted')
    paginator = Paginator(posts, 10)  # Show 10 posts per page
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    context = {
        'posts': page_obj
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
    post = get_object_or_404(Post, pk=pk, author=request.user)
    if request.method == 'POST':
        post.delete()
        messages.success(request, 'Your post has been deleted!')
        return redirect('profile')
    return render(request, 'blog/post_delete.html', {'post': post})