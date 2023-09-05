from __future__ import annotations

from typing import TYPE_CHECKING

from django.contrib.auth import get_user_model
from django.conf import settings
from django.core.mail import send_mail
from django.urls import reverse

from core.business_logic.exceptions import ConfirmationCodeExpired, ConfirmationCodeNotExists
from core.models import ConfirmationCode, Country, User

if TYPE_CHECKING:
    from core.business_logic.dto import RegistrationDTO
    
import logging
import time
import uuid



logger = logging.getLogger(__name__)


def create_user(data: RegistrationDTO) -> None:
    logger.info("Get user creation request.", extra={"user": str(data)})
    
    
    user_model: User = get_user_model()
    country = Country.objects.get(name=data.country)
    created_user = user_model.objects.create_user(
        username=data.username, password=data.password, email=data.email, first_name=data.first_name, 
        last_name=data.last_name, birth_date=data.birth_date, country=country, is_active=False, is_staff=False
    )
    
    confirmation_code = str(uuid.uuid4())
    code_expiration_time = int(time.time()) + settings.CONFIRMATION_CODE_LIFETIME
    ConfirmationCode.objects.create(code=confirmation_code, user=created_user, expiration_time=code_expiration_time)

    confirmation_url = settings.SERVER_HOST + reverse("confirm-signup") + f"?code={confirmation_code}"
    send_mail(
        subject="Confirm your email",
        message=f"Please confirm email by clicking the link below:\n\n{confirmation_url}",
        from_email=settings.EMAIL_FROM,
        recipient_list=[data.email],
    )


def confirm_user_registration(confirmation_code: str) -> None:
    try:
        code_data = ConfirmationCode.objects.get(code=confirmation_code)
    except ConfirmationCode.DoesNotExist as err:
        logger.error("Provided code doesn't exists.", exc_info=err, extra={"code": confirmation_code})
        raise ConfirmationCodeNotExists

    if time.time() > code_data.expiration_time:
        logger.info(
            "Provided expiration code expired.",
            extra={"current_time": str(time.time()), "code_expiration": str(code_data.expiration_time)},
        )
        raise ConfirmationCodeExpired

    user: User = code_data.user
    user.is_active = True
    user.save()

    code_data.delete()
