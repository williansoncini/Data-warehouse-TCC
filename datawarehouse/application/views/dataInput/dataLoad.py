from application.forms import CheckBoxForm
from application.services.database.stagingArea import createTableForEtl, importCsvFileInTableWithHeader,importCsvFileInTableWithOutHeader
from application.models import ColumnStagingArea, TableStagingArea, TemporaryFile, CsvFile
from django.shortcuts import redirect, render
from application.services.file.csvService import getColumnsFromCsvFile, getFirstTwentyLinesFromFile, getTypeOfColumnsFromCsvFile, makeDicWithColumnType, makeFakeColumnsFromCsvFile

def showDataFromFile(request):
    if request.method == 'POST':
        file = TemporaryFile.objects.get(pk=request.session['tempFilePk'])
        inputDataWithCsvHeader = bool(request.POST.get('checkbox',''))
        # print('Valor do checkBox: ',inputDataWithCsvHeader)
        typeColumns = getTypeOfColumnsFromCsvFile(file.filePath)

        if inputDataWithCsvHeader:
            columns = getColumnsFromCsvFile(file.filePath)
        else:
            columns = makeFakeColumnsFromCsvFile(file.filePath)
        
        
        (tableStagingArea,__) = TableStagingArea.objects.get_or_create(tableName=file.name)
        
        for index, column in enumerate(columns):
            (columnStagingArea,_) = ColumnStagingArea.objects.get_or_create(
                table=tableStagingArea,
                name=column,
                typeColumn=typeColumns[index])

        request.session['pkTableStagingArea'] = tableStagingArea.id

        dictionarieWithColumnsAndTypes = makeDicWithColumnType(columns,typeColumns)

        # request.session['dictionarieWithColumnsAndTypes'] = dictionarieWithColumnsAndTypes
        # request.session['nameTable'] = file.name

        createTableForEtl(file.name,dictionarieWithColumnsAndTypes)
        if inputDataWithCsvHeader:
            importCsvFileInTableWithHeader(file.filePath,file.name)
        else:
            importCsvFileInTableWithOutHeader(file.filePath,file.name)

        saveCSVFileInDataBase(file.name, file.size, inputDataWithCsvHeader)
        return redirect('../stagingArea')
        # return render(request, 'application/input/preUploadOnStagingArea.html')
    else:
        temporaryFile = TemporaryFile.objects.get(pk=request.session['tempFilePk'])
        firstTwentyRows = getFirstTwentyLinesFromFile(temporaryFile.filePath)

        checkBox = CheckBoxForm()
        return render(request, 'application/input/preUploadOnStagingArea.html', {
            'firstTwentyRows':firstTwentyRows,
            'checkbox': checkBox})

def showDataFromTable(request):
    if request.method == 'POST':
        print('POST')
    else:
        pass

def saveCSVFileInDataBase(name, size, withHeader):
    csvFile = CsvFile(
        name=name,
        size=size,
        withHeader=withHeader
    )
    csvFile.save()
    

