from django.views import View
from django.shortcuts import render, redirect

from application.models import TableDatawarehouse


class ListTableDatawarehouse(View):
    def get(self, request):
        tables = TableDatawarehouse.objects.all()

        return render(request, 'application/datawarehouse/tables/listTablesDatawarehouse.html',{
            'tables':tables
        })
