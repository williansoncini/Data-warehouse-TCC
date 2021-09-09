from django.http.response import HttpResponse
from application.models import Datamart
from django.shortcuts import redirect, render

def show(request):
    datamarts = Datamart.objects.all()

    return render(request, 'application/datamart/list.html', {
        'datamarts': datamarts
    })