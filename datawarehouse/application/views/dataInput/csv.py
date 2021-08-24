from os.path import splitext
from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from ...services.file.csvService import getColumnsFromCsvFile, getTypeOfColumnsFromCsvFile, makeDicWithColumnType
from ...services.database.stagingArea import importCsvFileInTable, createTableForEtl

def inputCsvFile(request):
    columns = []
    typeColumns = []
    if request.method == 'POST':
        try:
            nameFile = formatFileName(str(request.FILES['document']))
            filePathAfterUpload = saveCsvFileAndReturnFilePath(request.FILES['document'])
            columns = getColumnsFromCsvFile(filePathAfterUpload)
            typeColumns = getTypeOfColumnsFromCsvFile(filePathAfterUpload)
            dictionarieWithColumnsAndTypes = makeDicWithColumnType(columns,typeColumns)
            createTableForEtl(nameFile,dictionarieWithColumnsAndTypes)
            importCsvFileInTable(filePathAfterUpload, nameFile)
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
    # print('pasta: ',str(fileSystem.url))
    # filePathAfterUpload = str(fileSystem.url(newName)[1:])
    # print('pasta: ',fileSystem.path(newName))
    return fileSystem.path(newName)
    # return filePathAfterUpload

def getSucessMessage():
    sucessMessage = 'Arquivo carregado com sucesso!'
    return sucessMessage

def getFailMessage():
    failMessage = {'message': 'Falha ao carregar arquivo'}
    return failMessage

def formatFileName(name):
    nameWithOutExtension = splitext(name)[0]

    remove = [
        '.',
        ' ',
        '-'
    ]
    for char in remove:
        nameWithOutExtension = nameWithOutExtension.replace(char,'_')
    nameWithOutExtension = nameWithOutExtension.lower()
    return nameWithOutExtension