from typing import Any

from core.models import NotificationType
from django.db import migrations

DEFAULT_TYPES = ("admin", "likes", "retweets", "replies")


def populate_notification_types_table(apps: Any, schema_editor: Any) -> None:
    for type in DEFAULT_TYPES:
        NotificationType.objects.create(name=type)


def reverse_notification_types_table(apps: Any, schema_editor: Any) -> None:
    for type in DEFAULT_TYPES:
        NotificationType.objects.get(name=type).delete()


class Migration(migrations.Migration):
    dependencies = [
        ("core", "0002_populate_countries_table"),
    ]

    operations = [
        migrations.RunPython(
            code=populate_notification_types_table,
            reverse_code=reverse_notification_types_table,
        )
    ]
