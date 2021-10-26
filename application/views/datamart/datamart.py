from django.http.response import HttpResponse, JsonResponse
from application.models import Datamart
from django.shortcuts import redirect, render
from django.views import View

class DatamartView(View):
    
    def get(self, request, *args, **kwargs):
        datamarts = Datamart.objects.all()
    
        return render(request, 'application/datamart/list.html', {
            'datamarts': datamarts
        })

    def post(self, request):
        print(request)
        print('post')
        return HttpResponse('Bora mudar de tela?') 