from django.http.response import HttpResponse, JsonResponse
from application.models import Datamart, DatamartConnection
from django.shortcuts import redirect, render
from django.views import View

class DatamartUpdate(View):
    def get(self, request, datamart_id):
        datamart = Datamart.objects.get(pk=datamart_id)
        datamartConnection = DatamartConnection.objects.get(datamart_id=datamart_id)
        print(datamart.name)
        print(datamartConnection.ip)
        return render(request, 'application/datamart/update.html', {
            'datamart' : datamart,
            'connection': datamartConnection
        })

    def post(self, request):
        return HttpResponse('post sucesso')