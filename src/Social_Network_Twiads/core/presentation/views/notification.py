from django.contrib.auth.decorators import login_required
from django.shortcuts import render
from django.dispatch import receiver
from django.db.models.signals import post_save
from django.http import HttpResponse

from core.models import Notification, NotificationType, Like, Retweet, Tweet

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.http import HttpRequest

@login_required
def notification_controller(request):
    user = request.user
    notifications = user.notifications.order_by('-created_at')
    context = {
        'notifications': notifications
    }
    return render(request, 'notifications.html', context)


@receiver(post_save, sender=Like)
def like_notification_controller(sender, instance, created, **kwargs):
    if created:
        tweet = instance.tweet
        author = tweet.author
        tweet_url = f"/tweet/{tweet.id}/"
        notification_text = f"User {instance.user.username} liked your tweet: <a href='{tweet_url}'>{tweet.content}</a>"
        notification_type = NotificationType.objects.get(name="likes")
        notification = Notification.objects.create(text=notification_text, notification_type=notification_type)
        notification.user.set([author])

@receiver(post_save, sender=Retweet)
def retweet_notification_controller(sender, instance, created, **kwargs):
    if created:
        tweet = instance.tweet
        author = tweet.author
        tweet_url = f"/tweet/{tweet.id}/"
        notification_text = f"User {instance.user.username} retweeted your tweet: <a href='{tweet_url}'>{tweet.content}</a>"
        notification_type = NotificationType.objects.get(name="retweets")
        notification = Notification.objects.create(text=notification_text, notification_type=notification_type)
        notification.user.set([author])

@receiver(post_save, sender=Tweet)
def comment_notification_controller(sender, instance, created, **kwargs):
    if created and instance.parent_tweet is not None:
        tweet = instance.parent_tweet
        author = tweet.author
        tweet_url = f"/tweet/{tweet.id}/"
        notification_text = f"User {instance.author.username} commented your tweet: <a href='{tweet_url}'>{tweet.content}</a>"
        notification_type = NotificationType.objects.get(name="replies")
        notification = Notification.objects.create(text=notification_text, notification_type=notification_type)
        notification.user.set([author])
