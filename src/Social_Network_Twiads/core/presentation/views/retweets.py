from __future__ import annotations

from django.shortcuts import get_object_or_404, redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404, redirect
from django.views.decorators.http import require_http_methods
from core.models import Tweet, Retweet

from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from django.http import HttpRequest
    

def add_retweet_controller(request: HttpRequest, tweet_id: int) -> HttpResponse:
    user = request.user
    tweet = get_object_or_404(Tweet, pk=tweet_id, )
    retweet_count = tweet.retweets_count
    
    retweet = Retweet(user=user, tweet=tweet)
    retweet.save()
    tweet.retweets_count = retweet_count + 1
    tweet.save()
    
    current_page = request.META.get('HTTP_REFERER')
    return redirect(current_page)


@login_required
@require_http_methods(request_method_list=["POST"])
def delete_retweet_controller(request: HttpRequest, tweet_id: int) -> HttpResponse:
    user = request.user
    tweet = get_object_or_404(Tweet, pk=tweet_id)
    
    # Проверяем, есть ли ретвит от данного пользователя
    retweet = Retweet.objects.filter(user=user, tweet=tweet).first()
    if retweet:
        # Удаляем ретвит
        retweet.delete()
        tweet.retweets_count -= 1
        tweet.save()
    
    current_page = request.META.get('HTTP_REFERER')
    return redirect(current_page)
