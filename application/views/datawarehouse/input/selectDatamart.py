from django.shortcuts import redirect, render
from django.views.generic.base import View
from django.contrib import messages
from application.models import Datamart


class SelectDatamartToDatawarehouse(View):

    def get(self, request):
        datamarts = Datamart.objects.all()

        return render(request, 'application/datawarehouse/input/datamart/selectDatamart.html', {
            'datamarts': datamarts
        })

    def post(self, request):
        datamartSelected = request.POST.get('selectedDatamart')

        if datamartSelected == 'None':
            datamarts = Datamart.objects.all()
            messages.warning(request, 'Select a valid datamart!')
            return render(request, 'application/datawarehouse/input/datamart/selectDatamart.html', {
                'datamarts': datamarts
            })

        request.session['datawarehouse-datamartSelected'] = datamartSelected
        print(request.session['datawarehouse-datamartSelected'])

        return redirect('application:datawarehouse-import-datamart-query')
