from django.contrib import messages
from django.views import View
from django.shortcuts import redirect, render
import csv
from application.models import ColumnsDatawarehouse, TableDatawarehouse
from application.services.database.datawarehouse import createTableForEtl, importCsvFileInTableWithHeader
from application.services.file.csvService import getColumnsFromCsvFile, getTypeOfColumnsFromCsvFile, makeDicWithColumnType

class DatawarehouseDataLoad(View):
    def get(self, request):
        filePath = request.session['datawarehouse-csv-file-path']
        data = []
        with open(filePath) as file:
            csv_reader = csv.reader(file,delimiter=';')
            for row in csv_reader:
                data.append(row)
        print(data)
        return render(request,'application/datawarehouse/input/datamart/dataLoad.html',{
            'data':data
        })

    def post(self, request):
        filePath = request.session['datawarehouse-csv-file-path']
        tableName = request.session['datawarehouse-import-csv-table-name']

        typeColumns = getTypeOfColumnsFromCsvFile(filePath)
        columns = getColumnsFromCsvFile(filePath)

        dictionarieWithColumnsAndTypes = makeDicWithColumnType(columns,typeColumns)
        print(dictionarieWithColumnsAndTypes)
        createTableForEtl(tableName,dictionarieWithColumnsAndTypes)
        importCsvFileInTableWithHeader(filePath,tableName)

        try:
            tableDatawarehouse = TableDatawarehouse.objects.get(name=tableName)
            tableDatawarehouse.delete()
        except:
            pass
        
        tableDatawarehouse = TableDatawarehouse(name=tableName)
        tableDatawarehouse.save()
        print(tableDatawarehouse)
        for index, column in enumerate(columns):
            print(tableDatawarehouse)
            ColumnsDatawarehouse(
                table=tableDatawarehouse,
                name=column,
                type=typeColumns[index]).save()

        messages.success(request,'table imported successfully!')
        return redirect('application:datawarehouse-tables')