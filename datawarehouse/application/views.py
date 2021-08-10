# from django.http.response import HttpResponse, HttpResponseRedirect
from .services.file.csvService import makeCSVFile
from django.shortcuts import render,get_list_or_404
# from .models import Datamart
from .forms import QueryForm
# from .services.file.fileService import handle_uploaded_file
# from django.contrib import messages
from django.core.files.storage import FileSystemStorage
from .services.file.inputFileWithCsv import importCSVfile
from application.services.database.connectStagingArea import connect

# Create your views here.
def datamart_list(request):
    # datamarts = Datamart
    # return render(request,'datamart/list.html',{'datamarts':datamarts})
    return render(request,'application/datamart/list.html')

def fileinput(request):
    content = {}
    if request.method == 'POST':
        # file = fileForm(request.POST, request.FILES)

        file = request.FILES['document']
        # print(file.name)
        # print(file.size)
        # print(file.content_type)

        fs = FileSystemStorage()
        name = fs.save(file.name, file)
        # print('nome:',name)
        url = fs.url(name)

        importCSVfile(str(url[1:]))
        # if file.is_valid():
        #     handle_uploaded_file(request.FILES['document']) 
        #     messages.success(request,'Arquivo carregado com sucesso')
    # else:
    #     file = fileForm()
        content['mensagem'] = 'Arquivo carregado com sucesso!'
        
        # Testando a importação do arquivo no banco de dados


    return render(request, 'application/file/inputfile.html', content)

    # return render(request,'application/file/inputfile.html', {'form':file})


def queryInput(request):
    # if request.method == 'POST':
    if request.GET:
        queryText = request.GET['query']
        # queryForm = QueryForm(data=request.POST)

        conn = connect()
        cur = conn.cursor()

        # statement = "copy ({0}) to stdout with csv header".format(queryText)
        statement = "copy ({0}) to stdout delimiter ';'".format(queryText)
        
        makeCSVFile()

        with open('upload/testedocsv.csv','w',encoding='UTF8') as fileOutput:
            cur.copy_expert(statement,fileOutput)
            cur.close()
            conn.commit()
            conn.close()

        importCSVfile('upload/testedocsv.csv')
        # data = getDataFromQueryText()

        # if queryForm.is_valid():
        queryForm = QueryForm()
    else:
        queryForm = QueryForm()
    # queryForm = QueryForm()
    return render(request, 'application/input/query.html', {'queryForm': queryForm})