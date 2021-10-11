from django.core.files.storage import FileSystemStorage
from application.services.database.stagingArea import createTableForEtl, importCsvFileInTableWithHeader,importCsvFileInTableWithOutHeader, createTable
from application.models import ColumnDataMart, ColumnStagingArea, TableDataMart, TableStagingArea, TemporaryFile, CsvFile
from django.shortcuts import redirect, render
from application.services.file.csvService import getColumnsFromCsvFile, getFirstTwentyLinesFromFile, getTypeOfColumnsFromCsvFile, makeDicWithColumnType, makeFakeColumnsFromCsvFile

def showDataFromFile(request):
    if request.method == 'POST':
        createTableAutomatically = request.session['createTableAutomatically']
        file = TemporaryFile.objects.get(pk=request.session['tempFilePk'])
        inputDataWithCsvHeader = bool(request.POST.get('checkbox',''))
        filePath = file.filePath
        if createTableAutomatically:
            tableName = file.name
            typeColumns = getTypeOfColumnsFromCsvFile(filePath)

            if inputDataWithCsvHeader:
                columns = getColumnsFromCsvFile(filePath)
            else:
                columns = makeFakeColumnsFromCsvFile(filePath)

            (tableStagingArea,__) = TableStagingArea.objects.get_or_create(tableName=tableName)
            
            for index, column in enumerate(columns):
                (columnStagingArea,_) = ColumnStagingArea.objects.get_or_create(
                    table=tableStagingArea,
                    name=column,
                    typeColumn=typeColumns[index])

            request.session['pkTableStagingArea'] = tableStagingArea.id
            dictionarieWithColumnsAndTypes = makeDicWithColumnType(columns,typeColumns)

            createTableForEtl(tableName,dictionarieWithColumnsAndTypes)
            if inputDataWithCsvHeader:
                importCsvFileInTableWithHeader(filePath,tableName)
            else:
                importCsvFileInTableWithOutHeader(filePath,tableName)

            saveCSVFileInDataBase(tableName, file.size, inputDataWithCsvHeader)
            # deleteFile(filePath)
            return redirect('application:stagingArea')
        else:
            ############## MUDANÇA ################
            # ADICIONAR IF PARA PEGAR A TABELA QUE O USUÁRIO SELECIONOU EM VEZ DE CRIAR SEMPRE COM O ARQUIVO CSV 
            #Create table a partir da tabela que o usuário indicou
            datamartTable = TableDataMart.objects.get(name=request.session['tableSelected'])
            datamartColumns = ColumnDataMart.objects.filter(table=datamartTable)

            statement = 'CREATE TABLE {}('.format(datamartTable.name)
            lengthDatamartColumns = len(datamartColumns)
            for index, column in enumerate(datamartColumns):
                if index != lengthDatamartColumns-1:
                    statement+='{} {},'.format(column.name,column.type)
                else:
                    statement+='{} {});'.format(column.name,column.type)

            createTable(statement)
            
            if inputDataWithCsvHeader:
                importCsvFileInTableWithHeader(filePath,datamartTable.name)
            else:
                importCsvFileInTableWithOutHeader(filePath,datamartTable.name)

            (tableStagingArea,__) = TableStagingArea.objects.get_or_create(tableName=datamartTable.name)
            request.session['pkTableStagingArea'] = tableStagingArea.id
            return redirect('application:stagingArea')
    else:
        temporaryFile = TemporaryFile.objects.get(pk=request.session['tempFilePk'])
        firstTwentyRows = getFirstTwentyLinesFromFile(temporaryFile.filePath)

        return render(request, 'application/input/preUploadOnStagingArea.html', {
            'firstTwentyRows':firstTwentyRows})

def saveCSVFileInDataBase(name, size, withHeader):
    csvFile = CsvFile(
        name=name,
        size=size,
        withHeader=withHeader
    )
    csvFile.save()

def deleteFile(filePath):
    fileSystemStorage = FileSystemStorage()
    fileSystemStorage.delete(filePath)