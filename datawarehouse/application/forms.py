from django import forms

class fileForm(forms.Form):
    file = forms.FileField()

class QueryForm(forms.Form):
    # query = forms.CharField()
    # query = forms.CharField(max_length=1000,widget=forms.Textarea)
    # query = forms.CharField(max_length=1000,widget=forms.Textarea())
    query = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Coloque a query de consulta aqui'}))