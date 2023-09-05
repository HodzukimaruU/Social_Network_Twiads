from django import forms

from core.presentation.validators import ValidateMaxTagCount


class AddTweetForm(forms.Form):
    content = forms.CharField(label = 'Content', #will be displayed next to the form input field
                              max_length=400,
                              widget=forms.Textarea())
    tags = forms.CharField(label="Tags", required=False, widget=forms.Textarea, validators=[ValidateMaxTagCount(max_count=20)])


class EditTweetForm(forms.Form):
    content = forms.CharField(label = 'Content', #will be displayed next to the form input field
                              max_length=400,
                              widget=forms.Textarea())
    tags = forms.CharField(label="Tags", required=False, widget=forms.Textarea, validators=[ValidateMaxTagCount(max_count=20)])