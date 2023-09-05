from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth.decorators import login_required
from django.http import HttpResponseRedirect, HttpResponse, HttpResponseForbidden
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods
from django.urls import reverse

from core.models import Tweet
from core.presentation.forms import AddCommentForm
import logging



if TYPE_CHECKING:
    from django.http import HttpRequest
    
    
logger = logging.getLogger(__name__)


@login_required
@require_http_methods(request_method_list=["GET", "POST"])
def add_comment_controller(request: HttpRequest, tweet_id: int) -> HttpResponse:
    tweet = get_object_or_404(Tweet, id=tweet_id)
    
    if request.method == "POST":
        form = AddCommentForm(data=request.POST)
        if form.is_valid():
            comment_text = form.cleaned_data["comment"]
            comment = Tweet.objects.create(content=comment_text, author=request.user, parent_tweet=tweet)
            tweet.comments_count += 1
            tweet.save()
            return HttpResponseRedirect(redirect_to=reverse("get-tweet", args=[tweet_id]))
    else:
        form = AddCommentForm()
    
    context = {"form": form, "tweet": tweet}
    return render(request=request, template_name="comment.html", context=context)

@login_required
@require_http_methods(request_method_list=["POST"])
def delete_comment_controller(request: HttpRequest, tweet_id: int, comment_id: int) -> HttpResponse:
    tweet = get_object_or_404(Tweet, id=tweet_id)
    comment = get_object_or_404(Tweet, id=comment_id, parent_tweet=tweet)
    
    if comment.author == request.user:
        comment.delete()
        tweet.comments_count -= 1
        tweet.save()
        current_page = request.META.get('HTTP_REFERER')
        return redirect(current_page)
    else:
        return HttpResponseForbidden("Access denied")
