from django.views.generic import CreateView
from django.views.generic import DeleteView
from django.views.generic import DetailView
from django.views.generic import ListView
from django.views.generic import UpdateView


class FeedView(ListView):
    pass


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
