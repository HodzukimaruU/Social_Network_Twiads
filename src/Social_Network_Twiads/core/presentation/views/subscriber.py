from __future__ import annotations

from typing import TYPE_CHECKING

from django.http import HttpResponse
from django.shortcuts import get_object_or_404, render, redirect
from django.views.decorators.http import require_http_methods

from core.models import User
from core.business_logic.services import subscribe_and_unsubscribe
from core.business_logic.dto import SubscriberDTO


if TYPE_CHECKING:
    from django.http import HttpRequest


@require_http_methods(request_method_list=["GET","POST"])
def subscriber_controller(request: HttpRequest, username: str) -> HttpResponse:
    user = get_object_or_404(User, username=username)
    subscriber_user = request.user
    if request.method == "POST":
        data = SubscriberDTO(username=user.username, subscriber_username=subscriber_user.username)
        subscribe_and_unsubscribe(data=data)
    current_page = request.META.get('HTTP_REFERER')
    return redirect(current_page)


@require_http_methods(request_method_list=["GET"])
def followings_controller(request: HttpRequest, username: str) -> HttpResponse:
    user = get_object_or_404(User, username=username)
    following_users = user.subscriptions.all()
    
    context = {
        "user": user,
        "following_users": following_users,
    }
    
    return render(request=request, template_name='followings.html', context=context)


@require_http_methods(request_method_list=["GET"])
def followers_controller(request: HttpRequest, username: str) -> HttpResponse:
    user = get_object_or_404(User, username=username)
    followers = user.subscriber.all()
    
    context = {
        "user": user,
        "followers": followers,
    }
    
    return render(request=request, template_name='followers.html', context=context)
