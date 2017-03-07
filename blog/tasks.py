from django.core.mail import send_mail


def send_new_post_notifications(post):
    author = post.user
    for follower in author.followers.all():
        if follower.subscriber.email:
            send_mail('Новый пост от %s' % follower.subscriber.username,
                      """
                      Новый пост от %s можно прочитать по адресу:
                      %s
                      """ % (follower.subscriber.username, post.get_absolute_url()),
                      'servername@gde.to.tam',
                      [follower.subscriber.email],
                      fail_silently=False
                      )
