from django.db import models

from .base_model import BaseModel


class ConfirmationCode(BaseModel):
    """Confirmation code for registration email"""

    code = models.CharField(max_length=100, unique=True)
    expiration_time = models.PositiveIntegerField()

    user = models.ForeignKey(to="User", on_delete=models.CASCADE, related_name="confirmations")

    class Meta:
        db_table = "confirmation_codes"
