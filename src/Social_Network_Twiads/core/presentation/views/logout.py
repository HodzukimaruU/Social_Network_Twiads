from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth import logout
from django.http import HttpResponse
from django.shortcuts import redirect
from django.views.decorators.http import require_http_methods

if TYPE_CHECKING:
    from django.http import HttpRequest


@require_http_methods(["GET"])
def logout_controller(request: HttpRequest) -> HttpResponse:
    logout(request=request)
    return redirect(to="login")
