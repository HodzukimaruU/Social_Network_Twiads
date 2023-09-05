from django import forms


class LoginForm(forms.Form):
    username = forms.CharField(label="Username", max_length=150)
    password = forms.CharField(label="Enter password: ", widget=forms.PasswordInput, max_length=128)
