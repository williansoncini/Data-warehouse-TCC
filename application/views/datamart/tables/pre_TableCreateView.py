from django.contrib import messages
from django.views import View
from django.shortcuts import redirect, render

from application.models import Datamart, TableDataMart

class PreTableDatamartCreateView(View):
    def get(self, request):
        datamarts = Datamart.objects.all()
        return render(request, 'application/datamart/tables/pre-create.html',{
            'datamarts': datamarts
        })

    def post(self, request):
        datamartName = request.POST.get('datamartTable-datamart')
        tableName = request.POST.get('datamartTable-name')

        if datamartName == 'null':
            messages.warning(request, 'Select a valid Datamart')
            datamarts = Datamart.objects.all()
            return render(request, 'application/datamart/tables/pre-create.html',{
                'datamarts': datamarts
            })

        if tableName == '':
            messages.warning(request, 'Invalid table name')
            datamarts = Datamart.objects.all()
            return render(request, 'application/datamart/tables/pre-create.html',{
                'datamarts': datamarts
            })  

        try:
            checkIfTableExists = TableDataMart.objects.get(name = tableName)
            messages.warning(request, 'Table alredy exists')
            datamarts = Datamart.objects.all()
            return render(request, 'application/datamart/tables/pre-create.html',{
                'datamarts': datamarts
            })     
        except:
            checkIfTableExists = None
        
        if checkIfTableExists == None:
            datamart = Datamart.objects.get(name=datamartName)
            tableDatamart = TableDataMart(
                datamart=datamart,
                name=tableName
            )
            tableDatamart.save()
            request.session['tableDatamart-id-create-table-datamart'] = tableDatamart.id
            # request.session['name-create-table-datamart'] = tableName
        return redirect('application:datamart-tables-create',table_id=tableDatamart.id)
        # return render(request, 'application/datamart/tables/create.html')