from django.conf import settings
from django.db.models import ForeignKey
from django.db.models import Model, DateTimeField, CharField, TextField


class Post(Model):
    timestamp = DateTimeField(auto_now=False, auto_now_add=True)
    title = CharField(max_length=250)
    content = TextField()
    user = ForeignKey(settings.AUTH_USER_MODEL, default=1)

    def __str__(self):
        return self.title
