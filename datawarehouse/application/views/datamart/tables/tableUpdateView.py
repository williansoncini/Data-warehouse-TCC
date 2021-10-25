from django.shortcuts import redirect, render
from django.views import View

from application.models import ColumnDataMart, TableDataMart
from application.services.database.datamart import getDataFromDatamartTable

class TableDatamartUpdateView(View):
    def get(self, request, table_id):
        tableDatamart = TableDataMart.objects.get(pk=table_id)
        columnsDatamart = ColumnDataMart.objects.filter(table=tableDatamart)
        datamartTableName = tableDatamart.name 
        datamart = tableDatamart.datamart

        data = getDataFromDatamartTable(datamart, datamartTableName)

        return render(request, 'application/datamart/tables/update.html',{
            'tableDatamart':tableDatamart,
            'columnsDatamart':columnsDatamart,
            'data':data
        })

    def post(self, request, table_id):
        # tableDatamart = TableDataMart.objects.get(pk=table_id)
        # columnsDatamart = ColumnDataMart.objects.filter(table=tableDatamart)

        
        #Aqui vai realizar o create table no banco de dados
        return redirect('application:datamart-tables')