from django.conf.urls import url

from blog.views import FeedView, UserPostsView, SubscribeToUserView, CreatePostView, DetailPostView, EditPostView, \
    DeletePostView, MarkPostAsReadView

urlpatterns = [
    url(r'^feed$', FeedView.as_view(), name='feed'),
    url(r'^posts$', UserPostsView.as_view(), name='posts'),
    url(r'^posts/subscribe', SubscribeToUserView.as_view(), name='subscribe'),
    url(r'^posts/create$', CreatePostView.as_view(), name='create'),
    url(r'^posts/(?P<pk>\d+)', DetailPostView.as_view(), name='detail'),
    url(r'^posts/edit', EditPostView.as_view(), name='edit'),
    url(r'^posts/delete', DeletePostView.as_view(), name='delete'),
    url(r'^posts/(?P<pk>\d+)/read', MarkPostAsReadView.as_view(), name='mark-read'),

]
