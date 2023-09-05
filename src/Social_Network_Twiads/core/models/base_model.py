from django.db import models


class BaseModel(models.Model):

    """A model that determines the date of creation and the date of the last update"""

    created_at = models.DateTimeField(auto_now_add=True)  # auto_now_add=True - creates a label when a row is created in the database.
    updated_at = models.DateTimeField(auto_now=True)  # auto_now=True - updates the label each time a row in the database changes (saves).

    class Meta:
        abstract = True  # to not create a table
