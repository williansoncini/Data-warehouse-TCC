from django import forms

class fileForm(forms.Form):
    file = forms.FileField()