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
            subscription = Subscription.objects.get(subject=author, subscriber=self.request.user)
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

    def post(self, request, *args, **kwargs):
        if request.is_ajax() and request.user.is_authenticated():
            post_id = request.POST.get("post", "")
            if not post_id:
                return HttpResponse('Неверный id поста', status=400)
            request.user.blog_data.read_posts.add(int(post_id))
        return HttpResponse("ok")

    def get_queryset(self):
        if self.request.user.username != self.kwargs['username']:
            raise PermissionDenied("Только пользователь %s имеет доступ к этой странице" % self.kwargs['username'])
        follower = self.request.user
        subscribed_to = follower.following.values_list('subject', flat=True)

        return Post.objects.filter(user__in=subscribed_to)


class UserPostsView(BlogMixin, ListView):
    model = Post

    def get_queryset(self):
        username = self.kwargs.get('username')
        return Post.objects.filter(user__username=username)


class ProfileView(DetailView):
    template_name = "profile_page.html"
    model = Profile

    def get_object(self, queryset=None):
        return get_object_or_404(Profile, user__username=self.kwargs.get('username'))

    def post(self, request, *args, **kwargs):
        if request.is_ajax() and request.user.is_authenticated():
            if request.user == self.get_object().user:
                return HttpResponse('Нельзя подписаться на себя', status=400)
            subject_user = self.get_object().user
            subscription = Subscription.objects.toggle_subscribe(subject_user, request.user)
            data = {
                'subscribed': subscription,
                'author': subject_user.username
            }
            json_data = json.dumps(data)
            return HttpResponse(json_data, 'application/json')
        raise PermissionDenied


class CreatePostView(CreateView):
    model = Post
    form_class = PostForm

    def form_valid(self, form):
        post = form.save(commit=False)
        post.user = self.request.user
        post.save()
        return super(CreatePostView, self).form_valid(form)


class DetailPostView(BlogMixin, DetailView):
    model = Post


class EditPostView(UpdateView):
    model = Post
    form_class = PostForm


class DeletePostView(DeleteView):
    model = Post
