from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView

from blog.models import Post


class FeedView(ListView):
    model = Post

    def get_queryset(self):
        profile = self.request.user.profile
        Post.objects.filter(user_profile=profile)


class UserPostsView(ListView):
    pass


class CreatePostView(CreateView):
    pass


class DetailPostView(DetailView):
    pass


class EditPostView(UpdateView):
    pass


class DeletePostView(DeleteView):
    pass
