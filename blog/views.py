from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from blog.forms import PostForm
from blog.models import Post


class FeedView(ListView):
    model = Post

    def get_queryset(self):
        profile = self.request.user.profile
        return Post.objects.filter(profile__in=profile.subscriptions.all())


class UserPostsView(ListView):
    model = Post

    def get_queryset(self):
        profile = self.request.user.profile
        return Post.objects.filter(profile=profile)


class CreatePostView(CreateView):
    model = Post
    form_class = PostForm


class DetailPostView(DetailView):
    model = Post


class EditPostView(UpdateView):
    model = Post
    form_class = PostForm


class DeletePostView(DeleteView):
    model = Post
