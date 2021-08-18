from django.shortcuts import render, get_object_or_404, reverse
from django.views import generic, View
from django.http import HttpResponseRedirect
from django.contrib import messages
from .models import Post, Comment
from .forms import CommentForm


class PostList(generic.ListView):
    model = Post
    queryset = Post.objects.filter(status=1).order_by('-created_on')
    template_name = 'index.html'
    paginate_by = 6


class PostDetail(View):

    def get(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True
        return render(request,
                      'post_detail.html',
                      {
                         "post": post,
                         "liked": liked,
                         "comments": comments,
                         "commented": False,
                         "comment_form": CommentForm()
                      }
                      )

    def post(self, request, slug, *args, **kwargs):
        queryset = Post.objects.filter(status=1)
        post = get_object_or_404(queryset, slug=slug)
        comments = post.comments.filter(approved=True).order_by('created_on')
        liked = False
        if post.likes.filter(id=self.request.user.id).exists():
            liked = True

        comment_form = CommentForm(data=request.POST)

        if comment_form.is_valid():
            comment_form.instance.email = request.user.email
            comment_form.instance.name = request.user.username
            comment = comment_form.save(commit=False)
            comment.post = post
            comment.save()
            messages.add_message(request, messages.SUCCESS, 'Your comment has been sent!')
        else:
            comment_form = CommentForm()

        return render(request,
                      'post_detail.html',
                      {
                         "post": post,
                         "liked": liked,
                         "comments": comments,
                         "commented": True,
                         "comment_form": CommentForm()
                      }
                      )


class PostLike(View):
    def post(self, request, slug):
        post = get_object_or_404(Post, slug=slug)
        """
        If post.likes contains user: remove user
        else: add user to post.likes
        """
        if post.likes.filter(id=self.request.user.id).exists():
            # Remove user from post.likes (UNLIKE post)
            post.likes.remove(request.user)
        else:
            # Add user to post.likes (LIKE post)
            post.likes.add(request.user)
        return HttpResponseRedirect(reverse('post_detail', args=[slug]))
