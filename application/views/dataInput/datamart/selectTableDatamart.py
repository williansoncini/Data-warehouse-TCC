from django.contrib import messages
from django.shortcuts import redirect, render
from django.views.generic.base import View

from application.models import Datamart, TableDataMart

class SelectTableDatamart(View):

    def get(self, request):
        tables = TableDataMart.objects.all()

        return render(request, 'application/input/datamart/selectTableDatamart.html/', {
            'tables': tables
        })

    def post(self, request):
        createTableAutomatically = bool(request.POST.get('table-check'))
        request.session['createTableAutomatically'] = createTableAutomatically

        if createTableAutomatically == False:
            tableSelected = request.POST.get('selectedTable')
            if tableSelected == 'None':
                messages.warning(request,'Select a valid table!')
                tables = TableDataMart.objects.all()
                return render(request, 'application/input/datamart/selectTableDatamart.html/', {
                    'tables': tables
                })
            else:
                request.session['tableSelected'] = tableSelected

        return redirect('application:files-input')


