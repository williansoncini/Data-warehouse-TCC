from django.contrib import messages
from django.http.response import HttpResponse, JsonResponse
from application.models import Datamart, DatamartConnection
from django.shortcuts import redirect, render
from django.views import View
import psycopg2
from dotenv import load_dotenv
from os import getenv

class DatamartCreate(View):
    
    def get(self, request, *args, **kwargs):
        # messages.success(request,'teste') 
        
        return render(request, 'application/datamart/create.html')

    def post(self, request):
        checkbox = request.POST.get('datamart-check')
        name=request.POST.get('datamart-name','')
        datamartExistentInSystemDb = Datamart.objects.filter(name=name).first()
        
        if checkbox == 'on':

            if datamartExistentInSystemDb == None:
                load_dotenv()
                conn = getDefaultConectionDataMart()
                conn.autocommit = True

                cur = conn.cursor()
                cur.execute("SELECT DATNAME FROM pg_database where datname='{}'".format(name))
                datamartExistentInServerDb = cur.fetchone()

                if datamartExistentInServerDb == None:
                    dataMart = Datamart(name=name)
                    datamartConnection = getDefaultObjectConectionDataMart(dataMart)
                    
                    cur.execute('CREATE DATABASE {};'.format(name))
                    dataMart.save()
                    datamartConnection.save()
                else:
                    dataMart = Datamart(name=name)
                    datamartConnection = getDefaultObjectConectionDataMart(dataMart)
                    dataMart.save()
                    datamartConnection.save()
                cur.close()
                conn.close()
        else:
            if datamartExistentInSystemDb == None:
                host = request.POST.get('datamart-host','')
                port = request.POST.get('datamart-port','')
                username = request.POST.get('datamart-username')
                password = request.POST.get('datamart-password')

                conn = psycopg2.connect(
                    database=name,
                    host=host,
                    port=port,
                    user=username,
                    password=password
                )
                conn.autocommit = True

                cur = conn.cursor()
                cur.execute("SELECT DATNAME FROM pg_database where datname='{}'".format(name))
                datamartExistentInServerDb = cur.fetchone()

                if datamartExistentInServerDb != None:
                    dataMart = Datamart(name=name)
                    dataMart.save()
                    datamartConnection = DatamartConnection(
                        database=name,
                        host=host,
                        port=port,
                        username=username,
                        password=password,
                        datamart_id=dataMart
                    )
                    
                    datamartConnection.save()
                cur.close()
                conn.close()                    
            else:
                print('Datamart já existente: ', datamartExistentInSystemDb.name)
        return redirect('application:datamart-list')

def getDefaultConectionDataMart():
    return psycopg2.connect(
        database=getenv('SYSTEM_DATA_BASE_DATABASE'),
        host=getenv('SYSTEM_DATA_BASE_HOST'),
        port=getenv('SYSTEM_DATA_BASE_PORT'),
        user=getenv('SYSTEM_DATA_BASE_USERNAME'),
        password=getenv('SYSTEM_DATA_BASE_PASSWORD')
    )

def getDefaultObjectConectionDataMart(dataMart):
    return DatamartConnection(
        database=getenv('SYSTEM_DATA_BASE_DATABASE'),
        host=getenv('SYSTEM_DATA_BASE_HOST'),
        port=getenv('SYSTEM_DATA_BASE_PORT'),
        username=getenv('SYSTEM_DATA_BASE_USERNAME'),
        password=getenv('SYSTEM_DATA_BASE_PASSWORD'),
        datamart_id=dataMart
    )