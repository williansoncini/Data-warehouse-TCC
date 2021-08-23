from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from ...services.file.csvService import getColumnsFromCsvFile, getTypeOfColumnsFromCsvFile, makeDicWithColumnType
from ...services.database.stagingArea import importCsvFileInTable, createTableForEtl

def inputCsvFile(request):
    columns = []
    typeColumns = []
    if request.method == 'POST':
        try:
            nameFile = request.FILES['document']
            print('Nome do arquivo: ', nameFile)

            filePathAfterUpload = saveCsvFileAndReturnFilePath(request.FILES['document'])
            columns = getColumnsFromCsvFile(filePathAfterUpload)
            typeColumns = getTypeOfColumnsFromCsvFile(filePathAfterUpload)

            dictionarieWithColumnsAndTypes = makeDicWithColumnType(columns,typeColumns)

            createTableForEtl('TESTE_CSV',dictionarieWithColumnsAndTypes)
            
            importCsvFileInTable(filePathAfterUpload, 'TESTE_CSV')
            # print(columns)
            # print(typeColumns)
            return render(request, 'application/input/inputfile.html', {
                'message': getSucessMessage(),
                'columns': columns,
                'typeColumns': typeColumns
                })
        except OSError as err:
            print(err)
            return render(request, 'application/input/inputfile.html', getFailMessage())
    else:    
        return render(request, 'application/input/inputfile.html')

def saveCsvFileAndReturnFilePath(file):
    fileSystem = FileSystemStorage()
    newName = fileSystem.save(file.name, file)
    filePathAfterUpload = str(fileSystem.url(newName)[1:])
    return filePathAfterUpload

def getSucessMessage():
    sucessMessage = 'Arquivo carregado com sucesso!'
    return sucessMessage

def getFailMessage():
    failMessage = {'message': 'Falha ao carregar arquivo'}
    return failMessage
