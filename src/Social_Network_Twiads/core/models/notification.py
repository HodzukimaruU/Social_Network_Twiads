from django.db import models

from .base_model import BaseModel


class Notification(BaseModel):
    """Notification to user from admin or activity"""

    text = models.CharField(max_length=500, null=False)

    user = models.ManyToManyField(to="User", related_name="notifications")
    notification_type = models.ForeignKey(to="NotificationType", on_delete=models.CASCADE, related_name="notification_types")

    class Meta:
        db_table = "notifications"
