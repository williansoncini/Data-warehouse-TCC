from functools import total_ordering
from django import forms
from application.models import ColumnStagingArea, TypeData, CsvFile

# class inputFileForm(forms.Form):
#     file = forms.FileField(widget=forms.FileInput(attrs={'class':'teste'}))

class CheckBoxForm(forms.Form):
    checkbox = forms.BooleanField(label='Importar dados considerando o cabeçalho do arquivo?',required=False)

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
        model = CsvFile
        fields = ['name','size','withHeader']

class ColumnStagingAreaForm(forms.ModelForm):
    class Meta:
        model = ColumnStagingArea
        fields = ['name','typeColumn']

class TableStagingAreaForm(forms.ModelForm):
    class Meta:
        fields = '__all__'