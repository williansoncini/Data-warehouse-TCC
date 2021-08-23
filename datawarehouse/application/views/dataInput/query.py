import psycopg2
from ...services.file.csvService import makeNewCsvFile
from django.shortcuts import render
from ...forms import QueryForm
from application.services.database.stagingArea import connect

def inputFromQuerySQL(request):
    if request.GET:
        queryText = request.GET['query']

        conn = connect()
        cur = conn.cursor()
        statement = "copy ({0}) to stdout delimiter ';'".format(queryText)
        makeNewCsvFile()

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