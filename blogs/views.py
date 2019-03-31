from django.shortcuts import render, get_object_or_404
from django.http import HttpResponseRedirect, Http404
from django.urls import reverse
from django.contrib.auth.decorators import login_required

from .models import BlogPost
from .forms import BlogPostForm


def index(request):
    """The home page for Blog"""
    return render(request, 'blogs/index.html')


@login_required
def posts(request):
    """Show all posts"""
    posts = BlogPost.objects.filter(owner=request.user).order_by('-date_added')
    context = {'posts': posts}
    return render(request, 'blogs/posts.html', context)


@login_required
def post(request, post_id):
    """Show a single post."""
    post = get_object_or_404(BlogPost, id=post_id)
    if post.owner != request.user:
        raise Http404
    context = {'post': post}
    return render(request, 'blogs/post.html', context)


@login_required
def new_post(request):
    """Add a new post."""
    if request.method != 'POST':
        # No data submitted; create a blank form.
        form = BlogPostForm()
    else:
        # POST data submitted; process data.
        form = BlogPostForm(request.POST)
        if form.is_valid():
            new_post = form.save(commit=False)
            new_post.owner = request.user
            new_post.save()
            return HttpResponseRedirect(reverse('blogs:posts'))

    context = {'form': form}
    return render(request, 'blogs/new_post.html', context)


@login_required
def edit_post(request, post_id):
    """Edit an existing post."""
    post = get_object_or_404(BlogPost, id=post_id)
    if post.owner != request.user:
        raise Http404

    if request.method != 'POST':
        # Initial request; pre-fill form with the current post.
        form = BlogPostForm(instance=post)
    else:
        # POST data submitted; process data.
        form = BlogPostForm(instance=post, data=request.POST)
        if form.is_valid():
            form.save()
            return HttpResponseRedirect(reverse('blogs:posts'))

    context = {'post': post, 'form': form}
    return render(request, 'blogs/edit_post.html', context)
