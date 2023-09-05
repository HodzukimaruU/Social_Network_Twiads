from django.db import models

from .base_model import BaseModel


class Retweet(BaseModel):
    """Share another user's tweet on your own page"""

    user = models.ForeignKey(to="User", on_delete=models.CASCADE, related_name="retweets")
    tweet = models.ForeignKey(to="Tweet", on_delete=models.CASCADE, related_name="retweets")

    class Meta:
        db_table = "retweets"
