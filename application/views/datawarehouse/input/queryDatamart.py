from os import name, path
from django.contrib import messages
from django.views import View
from django.shortcuts import render, redirect
from application.models import ColumnDataMart, ColumnsDatawarehouse, Datamart, TableDataMart, TableDatawarehouse, TableStagingArea
# from application.services.database.datawarehouse import 
from application.services.database.datamart import exportSelectToCsv
from application.services.database.datawarehouse import createTableForEtl, importCsvFileInTableWithHeader
from application.services.file.csvService import getColumnsFromCsvFile, getTypeOfColumnsFromCsvFile, makeDicWithColumnType
from application.services.stringService import generateRandomString

class QueryDatamartDatawarehouse(View):
    def get(self, request):
        datamart = Datamart.objects.get(name=request.session['datawarehouse-datamartSelected'])
        tables = TableDataMart.objects.filter(datamart=datamart)

        tableAndColumns = []

        for table in tables:
            columns = ColumnDataMart.objects.filter(table=table)
            objeto = {
                'table': table,
                'columns': columns
            }
            tableAndColumns.append(objeto)

        return render(request, 'application/datawarehouse/input/datamart/query.html', {
            'tableAndColumns': tableAndColumns,
        })

    def post(self, request):
        try:
            datamart = Datamart.objects.get(name=request.session['datawarehouse-datamartSelected'])
            statementSelect = request.POST.get('statementSelect')
            nameFile = generateRandomString() + '.csv'
            filePath = path.dirname(__file__) + '/../../../../exports/'+ nameFile
            with open(filePath, 'w+') as csvFile:
                exportSelectToCsv(datamart, statementSelect, csvFile)
                request.session['datawarehouse-csv-file-path'] = filePath
                tableName = request.POST.get('table-name')
                request.session['datawarehouse-import-csv-table-name'] = tableName
        
            messages.success(request, 'Check data ✅')
            return redirect('application:datawarehouse-import-tables-data-load')
        except:
            messages.warning(request, 'Erro ao tentar exportar dados')
            return redirect('application:datawarehouse-import-datamart-query')