from django.contrib.auth.models import AbstractUser
from django.db import models

from .base_model import BaseModel


class User(BaseModel, AbstractUser):
    """User model which we add"""

    birth_date = models.DateField()
    avatar = models.ImageField(upload_to="profile/avatar/", null=True)
    subscribers_count = models.PositiveIntegerField(default=0)
    subscriptions_count = models.PositiveIntegerField(default=0)
    tweets_count = models.PositiveIntegerField(default=0)
    bio = models.CharField(max_length=400, null=True)

    subscriber = models.ManyToManyField(
        to="self",  # link to self
        symmetrical=False,  # relation are not symmetrical
        related_name="subscriptions",  # name to feedback
        db_table="subscriber_user",
    )
    country = models.ForeignKey(to="Country", on_delete=models.CASCADE, related_name="users")
    
    def to_dict(self):
        return {
            "avatar": self.avatar,
            "username": self.username,
            "first_name": self.first_name,
            "last_name": self.last_name,
            "email": self.email,
            "birth_date": self.birth_date,
            "country": self.country.name
        }

    class Meta:
        """Rename"""

        db_table = "users"
