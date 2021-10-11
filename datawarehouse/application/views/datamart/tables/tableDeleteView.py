from django.views import View
from django.shortcuts import render

from application.models import ColumnDataMart, TableDataMart

class TableDeleteView(View):
    def get(self,request,table_id):
        datamartTable = TableDataMart.objects.get(pk=table_id)
        columnsDatamart = ColumnDataMart.objects.filter(table=datamartTable)
        return render(request, 'application/datamart/tables/delete.html',{
            'datamartTable':datamartTable,
            'columnsDatamart':columnsDatamart
        })