from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View

from application.models import ColumnDataMart, TableDataMart
from application.services.database.datamart import checkExistentTable, deleteColumnDatamart

class DeleteColumnDatamartView(View):
    def get(self, request, table_id, column_id):
        column = ColumnDataMart.objects.get(pk=column_id)
        return render(request, 'application/datamart/tables/columns/deleteColumnDatamart.html',{
            'table_id':table_id,
            'column':column
        })

    def post(self, request, table_id, column_id):
        try:
            tableDatamart = TableDataMart.objects.get(pk=table_id)
            column = ColumnDataMart.objects.get(pk=column_id)

            tableName = tableDatamart.name
            columnName = column.name
            datamart = tableDatamart.datamart
            tableExists = checkExistentTable(datamart,tableName)
            if(tableExists):
                deletedColumn = deleteColumnDatamart(datamart, tableName, columnName)
                if (deletedColumn):
                    column.delete()
                    messages.success(request, "'{}' column has been deleted!")
                    return redirect('application:datamart-tables-update', table_id=table_id)
            else:
                messages.warning(request, "Table '{}' does not exists".format(tableName))
                return redirect('application:datamart-tables-update', table_id=table_id)
        except Exception as e:
            print(e)
            messages.warning(request, "Error at delete column '{}'".format(columnName))
            return redirect('application:datamart-tables-update', table_id=table_id) 
        