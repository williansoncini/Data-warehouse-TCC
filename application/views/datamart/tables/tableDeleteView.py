from django.contrib import messages
from django.views import View
from django.shortcuts import redirect, render

from application.models import ColumnDataMart, Datamart, TableDataMart
from application.services.database.datamart import connectInDatamartWithParameters, dropTableIfExists, getDataFromDatamartTable

class TableDatamartDeleteView(View):
    def get(self,request,table_id):
        datamartTable = TableDataMart.objects.get(pk=table_id)
        columnsDatamart = ColumnDataMart.objects.filter(table=datamartTable)
        datamartTableName = datamartTable.name 
        datamart = datamartTable.datamart

        data = getDataFromDatamartTable(datamart, datamartTableName)

        return render(request, 'application/datamart/tables/delete.html',{
            'datamartTable':datamartTable,
            'columnsDatamart':columnsDatamart,
            'data':data
        })

    def post(self, request, table_id):
        datamartTable = TableDataMart.objects.get(pk=table_id)
        columnsDatamart = ColumnDataMart.objects.filter(table=datamartTable)
        # datamart = Datamart.objects.get(pk=datamartTable.datamart.id)
        datamart = datamartTable.datamart
        datamart.database = str(datamart.database).lower()
        tableName = str(datamartTable.name).lower()
        datamartName = datamart.name

        print(datamart)
        dropTableIfExists(datamart, tableName)
        datamartTable.delete()
        columnsDatamart.delete()
        messages.success(request,"Table '{}' deleted at datamart '{}'!".format(tableName, datamartName))
        return redirect('application:datamart-tables')