from django import forms

from core.models import Country
from core.presentation.validators import ValidateFileExtension, ValidateFileSize


def get_countries() -> list:
    USER_COUNTRY_CHOICES = [(country.name, country.name) for country in Country.objects.all()]
    return USER_COUNTRY_CHOICES

class EditProfileForm(forms.Form):
    username = forms.CharField(max_length=30)
    first_name = forms.CharField(max_length=30)
    last_name = forms.CharField(max_length=30)
    birth_date = forms.DateField(label="Birth Date")
    email = forms.EmailField(label='Email')
    bio = forms.CharField(required=False, max_length=50)
    avatar = forms.ImageField(
       label='Avatar',
       required=False,
       allow_empty_file=False,
       validators=[ValidateFileExtension(["png", "jpg", "jpeg"]), ValidateFileSize(max_size=5_000_000)]
   )

    country = forms.ChoiceField(label='Country', choices=get_countries())
    change_email = forms.BooleanField(required=False, initial=False, widget=forms.HiddenInput())
