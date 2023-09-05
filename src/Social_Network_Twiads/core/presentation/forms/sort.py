from django import forms


SORT_CHOICES = (
    ("Newest", "Sort from new to old"),
    ("Likes", "Sort by likes count"),
)

class SortForm(forms.Form):
    sort_by = forms.ChoiceField(choices=SORT_CHOICES, widget=forms.RadioSelect)
