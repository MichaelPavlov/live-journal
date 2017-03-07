from django.conf import settings
from django.db.models import CASCADE
from django.db.models import ForeignKey
from django.db.models import Manager
from django.db.models import ManyToManyField
from django.db.models import Model, DateTimeField, CharField, TextField
from django.db.models import OneToOneField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse_lazy


class SubscriptionManager(Manager):
    def toggle_subscribe(self, subject, subscriber):
        subscription, created = self.get_or_create(subject=subject, subscriber=subscriber)
        if not created:
            subscription.delete()
            return False
        return True


class Profile(Model):
    user = OneToOneField(settings.AUTH_USER_MODEL, on_delete=CASCADE)

    def get_absolute_url(self):
        return reverse_lazy("blog:posts", kwargs={'username': self.user.username})

    def __str__(self):
        return self.profile.user.username


class Post(Model):
    timestamp = DateTimeField(auto_now=False, auto_now_add=True)
    title = CharField(max_length=250)
    content = TextField()
    user = ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=CASCADE)

    class Meta:
        ordering = ['-timestamp']

    def get_absolute_url(self):
        return reverse_lazy("blog:post-detail", kwargs={
            'username': self.profile.user.username,
            'pk': self.id,
        })

    def __str__(self):
        return self.title


class Subscription(Model):
    subject = ForeignKey(settings.AUTH_USER_MODEL, related_name="followers")
    subscriber = ForeignKey(settings.AUTH_USER_MODEL, related_name="following", on_delete=CASCADE)

    objects = SubscriptionManager()

    class Meta:
        unique_together = (('subject', 'subscriber',),)

    def __str__(self):
        return "%s to %s" % (self.subject.user.username, self.subject.user.subscriber)


class UserBlogData(Model):
    user = OneToOneField(settings.AUTH_USER_MODEL, on_delete=CASCADE)
    read_posts = ManyToManyField(Post)

    def __str__(self):
        return self.profile.user.username


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
        UserBlogData.objects.create(user=instance)
