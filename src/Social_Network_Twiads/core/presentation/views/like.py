from __future__ import annotations

from django.shortcuts import get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse

from core.models import Tweet, Like

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.http import HttpRequest


@login_required
def like_tweet_controller(request: HttpRequest, tweet_id: int) -> HttpResponse:
    tweet = get_object_or_404(Tweet, id=tweet_id)
    user = request.user
    
    like_count = tweet.likes_count

    existing_like = Like.objects.filter(tweet=tweet, user=user).first()
    if existing_like:
        existing_like.delete()
        tweet.likes_count = like_count - 1
    else:
        Like.objects.create(tweet=tweet, user=user)
        tweet.likes_count = like_count + 1

    tweet.save()

    current_page = request.META.get('HTTP_REFERER')
    return redirect(current_page)


from django.shortcuts import redirect, get_object_or_404
from django.views.decorators.http import require_GET
from django.db.models import Count

@login_required
@require_GET
def like_comment_controller(request, comment_id):
    comment = get_object_or_404(Tweet, id=comment_id)
    user = request.user
    
    like_count = comment.parent_tweet.comments.aggregate(likes_count=Count('likes'))['likes_count']

    existing_like = Like.objects.filter(tweet=comment, user=user).first()
    if existing_like:
        existing_like.delete()
        comment.parent_tweet.likes_count = like_count - 1
    else:
        Like.objects.create(tweet=comment, user=user)
        comment.parent_tweet.likes_count = like_count + 1

    comment.parent_tweet.save()

    current_page = request.META.get('HTTP_REFERER')
    return redirect(current_page)
