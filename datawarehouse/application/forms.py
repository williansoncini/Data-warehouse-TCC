from django import forms
from application.models import TypeData, csvFile

class fileForm(forms.Form):
    file = forms.FileField()

class QueryForm(forms.Form):
    # query = forms.CharField()
    # query = forms.CharField(max_length=1000,widget=forms.Textarea)
    # query = forms.CharField(max_length=1000,widget=forms.Textarea())
    query = forms.CharField(widget=forms.Textarea(attrs={'placeholder': 'Coloque a query de consulta aqui'}))

class TypeDataForm(forms.ModelForm):
    class Meta:
        model = TypeData
        fields = ('typeSimple','typeDataBase')

class csvForm(forms.ModelForm):
    class Meta:
        model = csvFile
        fields = ['name','size','updated','withHeader']