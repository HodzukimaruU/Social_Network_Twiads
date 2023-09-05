from __future__ import annotations

import logging

from typing import TYPE_CHECKING

from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseRedirect
from django.shortcuts import render, redirect, get_object_or_404
from django.views.decorators.http import require_http_methods
from django.core.paginator import Paginator
from django.contrib.auth.decorators import login_required
from django.urls import reverse
from django.db.models import Q

from core.business_logic.exceptions import ConfirmationCodeExpired, ConfirmationCodeNotExists
from core.models import Tweet, User
from core.presentation.converters import convert_data_from_form_to_dto
from core.business_logic.services import confirm_user_registration, edit_profile
from core.business_logic.dto import EditProfileDto
from core.presentation.forms import EditProfileForm, SortForm



if TYPE_CHECKING:
    from django.http import HttpRequest

logger = logging.getLogger(__name__)


@require_http_methods(request_method_list=["GET"])
def profile_controller(request: HttpRequest) -> HttpResponse:
    
    current_user = get_object_or_404(User, username=request.user)
    
    tweets = Tweet.objects.filter(Q(author=current_user), parent_tweet=None)
    retweets = Tweet.objects.prefetch_related('retweets').filter(retweets__user=current_user)

    tweets_and_retweets = tweets.union(retweets)
    
    form  = SortForm(request.GET)
    tweets_and_retweets = tweets_and_retweets.order_by('-created_at')
    
    paginator = Paginator(tweets, 2)
    page_number = request.GET.get('page', 1)
    page = paginator.get_page(page_number)

    context = {"tweets": tweets,
               "retweets": retweets,
               "form": form,
               "tweets": page,
               "tweets_and_retweets": page,
               "current_user": current_user
               }
    
    return render(request=request, template_name="profile.html", context=context)   


@login_required
@require_http_methods(request_method_list=["GET", "POST"])
def edit_profile_controller(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        if request.user.is_authenticated:
            user = request.user
            initial_data = user.to_dict()
            form = EditProfileForm(initial=initial_data)
            context = {"form": form}
            return render(request=request, template_name="edit_profile.html", context=context)
        else:
            return HttpResponse("You need to log in to edit your profile.")

    elif request.method == "POST":
        if request.user.is_authenticated:
            form = EditProfileForm(data=request.POST, files=request.FILES)
            if form.is_valid():
                data = convert_data_from_form_to_dto(EditProfileDto, data_from_form=form.cleaned_data)
                user = request.user
                if form.cleaned_data["change_email"]:
                   edit_profile(data=data, user=user)
                else:
                    edit_profile(data=data, user=user)
                    return HttpResponseRedirect(redirect_to=reverse("profile"))
            else:
                form = EditProfileForm(request.POST)
                context = {"form": form}
                return render(request=request, template_name="edit_profile.html", context=context)
            

@require_http_methods(["GET"])
def confirm_email_stub_controller(request: HttpRequest) -> HttpResponse:
    return HttpResponse("Confirmation email sent. Please confirm it by the link.")


@require_http_methods(["GET"])
def registration_confirmation_controller(request: HttpRequest) -> HttpResponse:
    confirmation_code = request.GET["code"]
    try:
        confirm_user_registration(confirmation_code=confirmation_code)
    except ConfirmationCodeNotExists:
        return HttpResponseBadRequest(content="Invalid confirmation code.")
    except ConfirmationCodeExpired:
        return HttpResponseBadRequest(content="Confirmation code expired.")

    return redirect(to="login")
