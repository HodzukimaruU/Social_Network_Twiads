from __future__ import annotations

from typing import TYPE_CHECKING

from django.http import HttpResponse, HttpResponseBadRequest
from django.shortcuts import redirect, render
from django.views.decorators.http import require_http_methods

if TYPE_CHECKING:
    from django.http import HttpRequest

from core.business_logic.dto import RegistrationDTO
from core.business_logic.exceptions import ConfirmationCodeExpired, ConfirmationCodeNotExists
from core.business_logic.services import confirm_user_registration, create_user
from core.presentation.converters import convert_data_from_form_to_dto
from core.presentation.forms import RegistrationForm


@require_http_methods(["GET", "POST"])
def registration_controller(request: HttpRequest) -> HttpResponse:
    if request.method == "GET":
        form = RegistrationForm()
        context = {"form": form}
        return render(request=request, template_name="signup.html", context=context)

    elif request.method == "POST":
        form = RegistrationForm(request.POST)
        if form.is_valid():
            data = convert_data_from_form_to_dto(dto=RegistrationDTO, data_from_form=form.cleaned_data)
            create_user(data=data)
            return redirect(to="confirm-stub")
        else:
            form = RegistrationForm(request.POST)
            context = {"form": form}
            return render(request=request, template_name="signup.html", context=context)


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
