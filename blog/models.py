from django.conf import settings
from django.db.models import ForeignKey
from django.db.models import Manager
from django.db.models import ManyToManyField
from django.db.models import Model, DateTimeField, CharField, TextField
from django.db.models import OneToOneField
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.urls import reverse_lazy


class Profile(Model):
    user = OneToOneField(settings.AUTH_USER_MODEL)
    read_posts = ManyToManyField('Post', related_name='profiles_read_this')

    def get_absolute_url(self):
        return reverse_lazy("blog:posts", kwargs={'username': self.user.username})


class Post(Model):
    timestamp = DateTimeField(auto_now=False, auto_now_add=True)
    title = CharField(max_length=250)
    content = TextField()
    profile = ForeignKey(Profile, default=1)

    class Meta:
        ordering = ['-timestamp']

    def get_absolute_url(self):
        return reverse_lazy("blog:post-detail", kwargs={
            'username': self.profile.user.username,
            'pk': self.id,
        })

    def __str__(self):
        return self.title


class SubscriptionManager(Manager):
    def toggle_subscribe(self, subject, subscriber):
        subscription, created = self.get_or_create(subject=subject, subscriber=subscriber)
        if not created:
            subscription.delete()
            return False
        return True


class Subscription(Model):
    subject = ForeignKey(Profile, related_name="followers")
    subscriber = ForeignKey(Profile, related_name="following")

    objects = SubscriptionManager()

    class Meta:
        unique_together = (('subject', 'subscriber',),)

    def __str__(self):
        return "%s to %s" % (self.subject.user.username, self.subject.user.subscriber)


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_user_profile(sender, instance, created, **kwargs):
    if created:
        Profile.objects.create(user=instance)
