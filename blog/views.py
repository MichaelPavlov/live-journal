import json

from django.contrib.auth import get_user_model
from django.core.exceptions import PermissionDenied
from django.http import HttpResponse
from django.shortcuts import get_object_or_404
from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from blog.forms import PostForm
from blog.models import Post, Profile, Subscription

User = get_user_model()


class BlogMixin(object):
    def get_context_data(self, **kwargs):
        context = super(BlogMixin, self).get_context_data(**kwargs)
        username = self.kwargs.get('username')
        author = User.objects.get(username=username)
        try:
            subscription = Subscription.objects.get(subject=author.profile, subscriber=self.request.user.profile)
        except:
            subscription = None
        context.update({
            'author': author,
            'subscription': subscription,
        })
        return context


class FeedView(ListView):
    model = Post
    template_name = "blog/feed_view.html"

    def get_queryset(self):
        if self.request.user.username != self.kwargs['username']:
            raise PermissionDenied("Только пользователь %s имеет доступ к этой странице" % self.kwargs['username'])
        profile = self.request.user.profile
        return Post.objects.filter(profile__in=profile.subscriptions.all())


class UserPostsView(BlogMixin, ListView):
    model = Post

    def get_queryset(self):
        username = self.kwargs.get('username')
        return Post.objects.filter(profile__user__username=username)


class ProfileView(DetailView):
    template_name = "profile_page.html"
    model = Profile

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user__username=self.kwargs.get('username'))

    def post(self, request, *args, **kwargs):
        if request.is_ajax() and request.user.is_authenticated():
            if request.user == self.get_object().user:
                return HttpResponse('Нельзя подписаться на себя', status=400)
            profile = self.get_object()
            subscription = Subscription.objects.toggle_subscribe(profile, request.user.profile)
            data = {
                'subscribed': subscription,
                'author': profile.user.username
            }
            json_data = json.dumps(data)
            return HttpResponse(json_data, 'application/json')
        raise PermissionDenied


class CreatePostView(CreateView):
    model = Post
    form_class = PostForm


class DetailPostView(BlogMixin, DetailView):
    model = Post


class EditPostView(UpdateView):
    model = Post
    form_class = PostForm


class DeletePostView(DeleteView):
    model = Post
