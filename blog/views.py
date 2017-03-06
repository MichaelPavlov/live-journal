from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from blog.forms import PostForm
from blog.models import Post

User = get_user_model()


class FeedView(ListView):
    model = Post
    template_name = "blog/feed_view.html"
    def get_queryset(self):
        if self.request.user.username != self.kwargs['username']:
            raise PermissionDenied("Только пользователь %s имеет доступ к этой странице" % self.kwargs['username'])
        profile = self.request.user.profile
        return Post.objects.filter(profile__in=profile.subscriptions.all())


class UserPostsView(ListView):
    model = Post

    def get_context_data(self, **kwargs):
        context = super(UserPostsView, self).get_context_data(**kwargs)
        username = self.kwargs.get('username')
        context['author'] = User.objects.get(username=username)
        return context

    def get_queryset(self):
        username = self.kwargs.get('username')
        return Post.objects.filter(profile__user__username=username)


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
