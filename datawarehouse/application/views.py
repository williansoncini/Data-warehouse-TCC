from .services.file.csvService import makeCSVFile
from django.shortcuts import render
from .forms import QueryForm
from django.core.files.storage import FileSystemStorage
from .services.file.inputFileWithCsv import importCSVfile
from application.services.database.connectStagingArea import connect

def datamart_list(request):
    return render(request,'application/datamart/list.html')

def fileinput(request):
    fileCsvInput = {}
    if request.method == 'POST':

        file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(file.name, file)
        url = fs.url(name)

        importCSVfile(str(url[1:]))
        fileCsvInput['mensagem'] = 'Arquivo carregado com sucesso!'
    return render(request, 'application/input/inputfile.html', fileCsvInput)

def queryInput(request):

    if request.GET:
        queryText = request.GET['query']

        conn = connect()
        cur = conn.cursor()
        statement = "copy ({0}) to stdout delimiter ';'".format(queryText)
        makeCSVFile()

        with open('upload/testedocsv.csv','w',encoding='UTF8') as fileOutput:
            cur.copy_expert(statement,fileOutput)
            cur.close()
            conn.commit()
            conn.close()

        importCSVfile('upload/testedocsv.csv')
        queryForm = QueryForm()
    else:
        queryForm = QueryForm()

    return render(request, 'application/input/inputQuery.html', {'queryForm': queryForm})

def listOfFormsImportations(request):

    return render(request, 'application/input/inputMenu.html')
