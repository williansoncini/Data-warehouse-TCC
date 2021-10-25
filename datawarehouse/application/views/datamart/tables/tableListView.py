from django.views import View
from django.shortcuts import render

from application.models import TableDataMart

class TableDatamartListView(View):
    def get(self,request):
        datamartTables = TableDataMart.objects.all()
        
        return render(request, 'application/datamart/tables/list.html',{
            'datamartTables':datamartTables
        })