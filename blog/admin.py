from django.contrib import admin

from blog.models import Post, UserBlogData, Profile

admin.site.register(Post)
admin.site.register(UserBlogData)
admin.site.register(Profile)
