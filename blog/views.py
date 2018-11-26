from django.shortcuts import render, get_object_or_404, redirect
from .models import Post, Comment, User
from .forms import PostForm, CommentForm
from django.contrib.auth.decorators import login_required
from django.utils import timezone
# from django.http import HttpResponse, JsonResponse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
#from celery.decorators import task



def post_list(request):
    posts = Post.objects.all().order_by('-created_date')
    return render(request, 'blog/post_list.html', {'posts': posts})

def post_detail(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user_name = request.user.username

    comment_list = post.comments.all()
    page = request.GET.get('page', 1)

    paginator = Paginator(comment_list, 5)
    try:
        comments = paginator.page(page) 
    except PageNotAnInteger:
        comments = paginator.page(1)
    except EmptyPage:
        comments = paginator.page(paginator.num_pages)

    # if request.method == "POST":
    #     form = CommentForm(request.POST)
    #     if form.is_valid():
    #         comment = form.save(commit=False)
    #         comment.post = post
    #         comment.author = user_name
    #         comment.publish()
    #         return redirect('posts:post_detail', pk=post.pk)
    # else:
    #     form = CommentForm()
    context = { 'post': post, 'comments': comments}
    return render(request, 'blog/post_detail.html', context)

@login_required
def post_new(request):
    if request.method == "POST":
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('posts:post_detail', pk=post.pk)
    else:
        form = PostForm()
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_edit(request, pk):
    post = get_object_or_404(Post, pk=pk)
    if request.method == "POST":
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.published_date = timezone.now()
            post.save()
            return redirect('posts:post_detail', pk=post.pk)
    else:
        form = PostForm(instance=post)
    return render(request, 'blog/post_edit.html', {'form': form})

@login_required
def post_publish(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.publish()
    return redirect('posts:post_detail', pk=pk)

@login_required
def post_remove(request, pk):
    post = get_object_or_404(Post, pk=pk)
    post.delete()
    return redirect('posts:post_list')

@login_required
def add_comment_to_post(request, pk):
    post = get_object_or_404(Post, pk=pk)
    user_name = request.user.username
    if request.method == "POST":
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = user_name
            comment.publish(comment) # for async in DB
            return redirect('posts:post_detail', pk=post.pk)
    else:
        form = CommentForm()
    return render(request, 'blog/add_comment_to_post.html', {'form': form})

# def add_reply_to_comment(request):
#     if request.is_ajax():
#         comment = CommentForm(request.POST or None)
#         reply_text = request.POST.get('reply_text')
#         id = request.POST.get('id')
#         parent_id = request.POST.get('parent_id')
#         parent = Comment.objects.get(id=parent_id)
#         parent.children += 1
#         parent.save()
#         if comment.is_valid() and request.user.is_authenticated:
#             comment = Comment.objects.create(comment_text=reply_text, destination=id, user=request.user, parent_id=parent_id, parent_comment=parent)
#             username = str(request.user)
#             return JsonResponse({'reply_text': reply_text, 'username': username})
#         else:
#             return HttpResponse()

# @login_required
# def add_reply_to_comment(request, pk):
#     comment = get_object_or_404(Comment, pk=pk)
#     user_name = request.user.username
#     if request.method == "POST":
#         form = CommentForm(request.POST)
#         if form.is_valid():
#             comment = form.save(commit=False)
#             comment.post = post
#             comment.author = user_name
#             comment.publish()
#             return redirect('posts:post_detail', pk=post.pk)
#     else:
#         form = CommentForm()
#     return render(request, 'blog/add_comment_to_post.html', {'form': form})


@login_required
def comment_remove(request, pk):
    comment = get_object_or_404(Comment, pk=pk)
    comment.delete()
    return redirect('posts:post_detail', pk=comment.post.pk)

# def list_comments(request, self):
#     comment_list = self.comments.all()
#     page = request.GET.get('page', 1)

#     paginator = Paginator(comment_list, 5)
#     try:
#         comments = paginator.page(page) 
#     except PageNotAnInteger:
#         comments = paginator.page(1)
#     except EmptyPage:
#         comments = paginator.page(paginator.num_pages)
#     context =  {}
#     return render(request, 'blog/post_detail.html', context)