from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View

from application.models import ColumnDataMart, TableDataMart

class CreateColumnDatamartView(View):
    def get(self, request, table_id):
        
        return render(request, 'application/datamart/tables/columns/create.html',{
            'table_id':table_id
        })

    def post(self, request, table_id):
        columnName = request.POST.get('columnName')
        columnType = request.POST.get('columnType')

        columnExists = ColumnDataMart.objects.filter(
            table = table_id,
            name = columnName
        ).first()

        print(columnExists)
        if (columnExists == None):
            tableDatamart = TableDataMart.objects.get(pk=table_id)
            columnDataMart = ColumnDataMart.objects.create(
                table = tableDatamart,
                name = columnName,
                type = columnType
            )
            print('criou?')
            messages.success(request, "Column '{}' create!".format(columnName))
            return redirect('application:datamart-tables-create', table_id=table_id)
        else:
            print()
            messages.warning(request, 'Column already exists!')
            return render(request, 'application/datamart/tables/columns/create.html',{
            'table_id':table_id
        })
        