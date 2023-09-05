from django.db import models

from .base_model import BaseModel


class Like(BaseModel):
    """Rating kite tweet"""

    user = models.ForeignKey(to="User", on_delete=models.CASCADE, related_name="likes")
    tweet = models.ForeignKey(to="Tweet", on_delete=models.CASCADE, related_name="likes")

    class Meta:
        db_table = "likes"
