from django import forms


class TagForm(forms.ModelForm):
    name = forms.CharField(max_length=50)
    
    def __str__(self):
        return self.name #to return name while you call to tag

