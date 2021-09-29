from django.contrib import messages
from django.http.response import HttpResponse, JsonResponse
import psycopg2
from application.models import Datamart, DatamartConnection
from django.shortcuts import redirect, render
from django.views import View

class DatamartUpdate(View):
    def get(self, request, datamart_id):
        datamart = Datamart.objects.get(pk=datamart_id)
        datamartConnection = DatamartConnection.objects.get(datamart_id=datamart_id)
        print(datamart.name)
        # print(datamartConnection.ip)
        return render(request, 'application/datamart/update.html', {
            'datamart' : datamart,
            'connection': datamartConnection
        })

    def post(self, request, datamart_id):
        datamart = Datamart.objects.get(pk=datamart_id)
        datamartConnection = DatamartConnection.objects.get(datamart_id=datamart_id)

        name=request.POST.get('datamart-name','')
        host = request.POST.get('datamart-host','')
        port = request.POST.get('datamart-port','')
        username = request.POST.get('datamart-username')
        password = request.POST.get('datamart-password')
        oldName = datamart.name

        if datamart.name != name:
            datamart.name = name

        if datamartConnection.host != host:
            datamartConnection.host = host

        if datamartConnection.port != port:
            datamartConnection.port = port

        if datamartConnection.username != username:
            datamartConnection.username = username

        if datamartConnection.password != password:
            datamartConnection.password = password

        #Fazer uma conexão com o banco de dados, para ver se ele irá de fato funcionar
        try:
            conn = psycopg2.connect(
                database=name,
                host=host,
                port=port,
                user=username,
                password=password
            )
            conn.autocommit = True
            cur = conn.cursor()
            #Fazer o alter database
            # cur.execute("alter database {} rename to {}".format(oldName, datamart.name))

            #Consultar o database
            cur.execute("SELECT DATNAME FROM pg_database where datname='{}'".format(name))
            datamartExistentInServerDb = cur.fetchone()
            cur.close()
            conn.close()
            if datamartExistentInServerDb != None:
                datamart.save()
                datamartConnection.save()   
                # messages.success(request,'teste')
                return redirect('application:datamart-list')
            else:
                #Retornar com mensagem de erro
                return render(request, 'application/datamart/update.html', {
                    'datamart' : datamart,
                    'connection': datamartConnection
                })
        except:
            print('erro irmão')
       
