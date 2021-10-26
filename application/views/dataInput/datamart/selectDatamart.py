from django.shortcuts import redirect, render
from django.views.generic.base import View
from django.contrib import messages

from application.models import Datamart

class SelectDatamart(View):

    def get(self, request):
        datamarts = Datamart.objects.all()

        return render(request, 'application/input/datamart/selectDatamart.html/', {
            'datamarts': datamarts
        })

    def post(self, request):
        datamartSelected = request.POST.get('selectedDatamart')
        
        if datamartSelected == 'None':
            datamarts = Datamart.objects.all()
            messages.warning(request, 'Select a valid datamart!')
            return render(request, 'application/input/datamart/selectDatamart.html/', {
                'datamarts': datamarts
            })

        request.session['datamartSelected'] = datamartSelected

        return redirect('application:select-table-datamart')


