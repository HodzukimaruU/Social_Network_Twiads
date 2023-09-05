from django import forms
from core.models import NotificationType


class NotificationFilterForm(forms.Form):
    notification_type = forms.ModelChoiceField(queryset=NotificationType.objects.all(), required=False)
