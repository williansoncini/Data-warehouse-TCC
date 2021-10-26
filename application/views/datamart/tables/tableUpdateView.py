from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View

from application.models import ColumnDataMart, TableDataMart
from application.services.database.datamart import checkExistentTable, getDataFromDatamartTable, renameTable

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
        try:
            tableDatamart = TableDataMart.objects.get(pk=table_id)
            newTableName = request.POST.get('datamartTable-name')
            oldTableName = tableDatamart.name

            if(oldTableName == newTableName):
                messages.success(request,"Table '{}' has not modified!".format(oldTableName))
                return redirect('application:datamart-tables')

            datamart = tableDatamart.datamart
            existentTable = checkExistentTable(datamart, oldTableName)
            if (existentTable):
                renameTable(datamart, oldTableName, newTableName)
                tableDatamart.name = newTableName
                tableDatamart.save()
                messages.success(request, "Table '{}' renomed to '{}'".format(oldTableName, newTableName))
                return redirect('application:datamart-tables')
            else:
                messages.warning(request, "Table '{}' not found at database!".format(oldTableName))
                redirect('application:datamart-tables')
        except Exception as e:
            print(e)
            messages.warning(request, 'Error at rename table!')
            return redirect('application:datamart-tables')