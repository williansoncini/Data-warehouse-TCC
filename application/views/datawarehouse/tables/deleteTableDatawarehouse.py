from django.contrib import messages
from django.views import View
from django.shortcuts import redirect, render

from application.models import ColumnDataMart, ColumnsDatawarehouse, Datamart, TableDataMart, TableDatawarehouse
from application.services.database.datawarehouse import getDataFromDatamartTable , dropTableIfExists

class DatawarehouseDeleteTable(View):
    def get(self,request,table_id):
        table = TableDatawarehouse.objects.get(pk=table_id)
        columns = ColumnsDatawarehouse.objects.filter(table=table)

        data = getDataFromDatamartTable(table.name)

        return render(request, 'application/datawarehouse/tables/deleteTableDatawarehouse.html',{
            'table':table,
            'columns':columns,
            'data':data
        })

    def post(self, request, table_id):
        table = TableDatawarehouse.objects.get(pk=table_id)
        columns = ColumnsDatawarehouse.objects.filter(table=table)
        tableName = str(table.name).lower()
        dropTableIfExists(tableName)
        table.delete()
        columns.delete()
        messages.success(request,"Table '{}' deleted!".format(tableName))
        return redirect('application:datawarehouse-tables')