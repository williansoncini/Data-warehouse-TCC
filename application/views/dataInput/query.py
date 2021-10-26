from string import ascii_uppercase, digits,ascii_letters
from random import choices
from django.contrib import messages
from django.views.generic.base import View
import psycopg2

from application.models import ExtractConnection, TemporaryFile
from ...services.file.csvService import makeNewCsvFile
from django.shortcuts import redirect, render
from ...forms import QueryForm
from application.services.database.stagingArea import connect

class QueryInput(View):
    def get(self, request):
        extractConnections = ExtractConnection.objects.all()
        # queryForm = QueryForm()
        return render(request, 'application/input/inputQuery.html', {
            'extractConnections': extractConnections
        })

    def post(self, request):
        selectedExtractConnection = request.POST.get('selectExtractConnection')
        if selectedExtractConnection == 'None':
            extractConnections = ExtractConnection.objects.all()
            messages.warning(request,'Select a valida connection!')
            return render(request, 'application/input/inputQuery.html', {
                'extractConnections': extractConnections
            })

        queryText = request.POST.get('statementSelect')
        if 'select' not in queryText or 'insert into' in queryText:
            extractConnections = ExtractConnection.objects.all()
            messages.warning(request,'Input a valid query!')
            return render(request, 'application/input/inputQuery.html', {
                'extractConnections': extractConnections
            })

        extractConnection = ExtractConnection.objects.get(name=selectedExtractConnection)
        randomName = self.generateRandomNameForFile()
        filePath ='upload/'+randomName+'.csv' 
        with open(filePath,'w+',encoding='UTF8') as fileOutput:
            self.exportCsvFromDatabase(extractConnection, queryText, fileOutput)

        tempFile = TemporaryFile(
            name = randomName,
            filePath= filePath
        )
        tempFile.save()

        request.session['tempFilePk'] = tempFile.id
        return redirect('application:data_load')

    def exportCsvFromDatabase(self, connection, query, file):
        database = connection.database
        host = connection.host
        port = connection.port
        user = connection.user
        password = connection.password

        conn = psycopg2.connect(
            database=database,
            host=host,
            port=port,
            user=user,
            password=password
        )
        sql = "COPY ({}) to stdout WITH CSV HEADER DELIMITER ';'".format(query)
        cur = conn.cursor()
        cur.copy_expert(sql, file)
        cur.close()
        conn.commit()
        conn.close()  

    def generateRandomNameForFile(self):
        numberChars = 10
        stringRandom = ''.join(choices(ascii_letters, k=numberChars))
        return stringRandom
        