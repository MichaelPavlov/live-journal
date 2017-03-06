from django.conf.urls import url

from blog.views import FeedView, UserPostsView, CreatePostView, DetailPostView, EditPostView, DeletePostView

urlpatterns = [
    url(r'^feed$', FeedView.as_view(), name='feed'),
    url(r'^posts$', UserPostsView.as_view(), name='posts'),  # subscribe тут же в метод post
    url(r'^posts/create$', CreatePostView.as_view(), name='create'),
    url(r'^posts/(?P<pk>\d+)', DetailPostView.as_view(), name='detail'),  # mark_as_read тут же в метод post
    url(r'^posts/edit', EditPostView.as_view(), name='edit'),
    url(r'^posts/delete', DeletePostView.as_view(), name='delete'),

]
