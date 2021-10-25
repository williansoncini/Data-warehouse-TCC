from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View

from application.models import ColumnDataMart, TableDataMart
from application.services.database.datamart import alterTypeFromTable, renameColumnFromTable

class UpdateColumnDatamartView(View):
    def get(self, request, table_id, column_id):
        column = ColumnDataMart.objects.get(pk=column_id)
        return render(request, 'application/datamart/tables/columns/updateColumnDatamart.html',{
            'table_id':table_id,
            'column':column
        })

    def post(self, request, table_id, column_id):
        tableDatamart = TableDataMart.objects.get(pk=table_id)
        datamart = tableDatamart.datamart
        column = ColumnDataMart.objects.get(pk=column_id)
        oldColumnName = column.name

        newColumnName = request.POST.get('columnName')
        newColumnType = request.POST.get('columnType','')

        if (column.name == newColumnName):
            if (column.type != newColumnType):
                try:
                    alterTypeFromTable(datamart, tableDatamart.name, oldColumnName, newColumnType)
                    column.type = newColumnType
                    column.save()
                    messages.success(request, "Column '{}' type updated to '{}'!".format(column.name, column.type))
                    return redirect('application:datamart-tables-update', table_id=table_id)
                except:
                    messages.warning(request, 'Type incompatible with table data!')
                    return render(request, 'application/datamart/tables/columns/updateColumnDatamart.html',{
                        'table_id':table_id,
                        'column':column
                    })
            else:
                messages.success(request, "Column '{}' not change!".format(column.name))
                return redirect('application:datamart-tables-update', table_id=table_id)

        columnExists = ColumnDataMart.objects.filter(
            table = table_id,
            name = newColumnName
        ).first()

        if (columnExists == None):
            if (column.type != newColumnType):
                alterTypeFromTable(datamart, tableDatamart.name, oldColumnName, newColumnType)
                column.type = newColumnType
                column.save()

            column.name = newColumnName
            column.save()
            renameColumnFromTable(datamart, tableDatamart.name, oldColumnName, newColumnName)

            messages.success(request, "Column '{}' updated!".format(newColumnName))
            return redirect('application:datamart-tables-update', table_id=table_id)
        else:
            messages.warning(request, 'Column already exists!')
            return render(request, 'application/datamart/tables/columns/updateColumnDatamart.html',{
                'table_id':table_id,
                'column':column
            })
        