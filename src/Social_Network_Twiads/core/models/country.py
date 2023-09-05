from django.db import models

from .base_model import BaseModel


class Country(BaseModel):
    name = models.CharField(max_length=60, unique=True)

    class Meta:
        db_table = "countries"
