import psycopg2
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

        conn = psycopg2.connect(
            host='localhost',
            database='datamart_test',
            user='postgres',
            password='123')
        # importCSVfile('upload/testedocsv.csv')

        conn = connect()
        cur = conn.cursor()
        cur.execute('SELECT * FROM TESTE_CSV')
        dados = cur.fetchall()
        print(dados)
        print(type(dados))

        cur.execute("select column_name from information_schema.columns where table_name = 'teste_csv'")
        colunas = cur.fetchall()
        print(colunas)
        cur.close()
        conn.commit()

        queryForm = QueryForm()
        mensagem = 'Query carregada com sucesso!'
        return render(request, 'application/input/inputQuery.html', {
            'queryForm': queryForm, 
            'mensagem': mensagem, 
            'colunas':colunas, 
            'dados': dados})
    else:
        queryForm = QueryForm()
        return render(request, 'application/input/inputQuery.html', {'queryForm': queryForm})

def listOfFormsImportations(request):
    queryForm = QueryForm()
    fileCsvInput = {}
    if request.method == 'POST':

        file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(file.name, file)
        url = fs.url(name)

        importCSVfile(str(url[1:]))
        fileCsvInput['mensagem'] = 'Arquivo carregado com sucesso!'
        return render(request, 'application/input/inputMenu.html', {'queryForm': queryForm, 'messagem': fileCsvInput})

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
        return render(request, 'application/input/inputMenu.html', {'queryForm': queryForm})

def getMenuInput(request):

    return render(request, 'application/input/menu.html')

def getHome(request):
    return render(request, 'application/home.html')

def inputDumpFile(request):
    retorno = {}
    if request.method == 'POST':

        file = request.FILES['dumpFile']
        fs = FileSystemStorage()
        name = fs.save(file.name, file)
        url = fs.url(name)

        # importCSVfile(str(url[1:]))
        # Aqui tem que fazer um tratamento de dados para não aceitar '`'
        with open (str(url[1:]),'r',encoding='UTF8') as dumpFile:
            conn = connect()
            cur = conn.cursor()
            cur.execute("""{}""".format(dumpFile.read().replace('`','')))
            cur.close()
            conn.commit()
            conn.close()

        retorno['mensagem'] = 'Arquivo DUMP carregado com sucesso!'

    return render(request, 'application/input/inputDump.html',retorno)