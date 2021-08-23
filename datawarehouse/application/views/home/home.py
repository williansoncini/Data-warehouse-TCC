from django.shortcuts import render
from ...forms import QueryForm, TypeDataForm

def getHome(request):
    form = TypeDataForm()

    return render(request, 'application/home.html', {'form': form})