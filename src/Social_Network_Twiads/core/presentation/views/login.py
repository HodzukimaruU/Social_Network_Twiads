from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth import login
from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

if TYPE_CHECKING:
    from django.http import HttpRequest

from core.business_logic.dto import LoginDTO
from core.business_logic.exceptions import InvalidAuthCredentials
from core.business_logic.services import authenticate_user
from core.presentation.converters import convert_data_from_form_to_dto
from core.presentation.forms import LoginForm


@require_http_methods(["GET", "POST"])
def login_controller(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        form = LoginForm()
        context = {"form": form}
        return render(request=request, template_name="signin.html", context=context)

    else:
        form = LoginForm(request.POST)
        if form.is_valid():
            data = convert_data_from_form_to_dto(dto=LoginDTO, data_from_form=form.cleaned_data)

            try:
                user = authenticate_user(data=data)
            except InvalidAuthCredentials:
                return HttpResponseBadRequest(content="Invalid credentials.")

            login(request=request, user=user)

            return redirect(to="home")
        else:
            context = {"form": form}
            return render(request=request, template_name="signin.html", context=context)
