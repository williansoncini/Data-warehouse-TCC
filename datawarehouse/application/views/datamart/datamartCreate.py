from django.contrib import messages
from application.models import Datamart
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
        checkboxCreateDatamartUsingDefaultConnection = request.POST.get('datamart-check')
        datamartName=request.POST.get('datamart-name','')
        database = request.POST.get('datamart-databaseName','')
        datamartExistentInSystemDb = Datamart.objects.filter(name=datamartName).first()
        
        if checkboxCreateDatamartUsingDefaultConnection == 'on':
            if datamartExistentInSystemDb == None:                
                datamartExistentInServerDb = getDatabaseIfExistsFromDefaultServerConnection(database)
                datamart = formingDatamartWithDefaultServerConnection(datamartName,database)                 
                if datamartExistentInServerDb == None:
                    datamartSavedBoolean = tryCreateDatabaseFromDatamartReturningBoolean(datamart)
                    if datamartSavedBoolean:
                        messages.success(request,'Data mart saved!')
                        datamart.save()
                else:
                    messages.success(request,'Data mart saved!')
                    datamart.save()
            else:
                print('Datamart já existente: ', datamartExistentInSystemDb.name)
                messages.warning(request,'Data mart already exists!')
        else:
            if datamartExistentInSystemDb == None:
                host = request.POST.get('datamart-host','')
                port = request.POST.get('datamart-port','')
                user = request.POST.get('datamart-username')
                password = request.POST.get('datamart-password')

                databaseOrNone = getDatabaseIfExistsFromParametersConnection(database,host,port,user,password)

                if databaseOrNone != None:
                    dataMart = formingDatamartWithParameters(datamartName,database,host,port,user,password)
                    messages.success(request,'Data mart saved!')
                    dataMart.save()
            else:
                print('Datamart já existente: ', datamartExistentInSystemDb.name)
                messages.warning(request,'Data mart already exists!')
        return redirect('application:datamart-list')

def getDefaultConectionDataMart():
    load_dotenv()
    return psycopg2.connect(
        database=getenv('SYSTEM_DATA_BASE_DATABASE'),
        host=getenv('SYSTEM_DATA_BASE_HOST'),
        port=getenv('SYSTEM_DATA_BASE_PORT'),
        user=getenv('SYSTEM_DATA_BASE_USERNAME'),
        password=getenv('SYSTEM_DATA_BASE_PASSWORD')
    )

def getDatabaseIfExistsFromDefaultServerConnection(databaseName):
    conn = getDefaultConectionDataMart()
    cur = conn.cursor()
    cur.execute("SELECT DATNAME FROM pg_database where datname='{}'".format(databaseName))
    databaseOrNone = cur.fetchone()
    cur.close()
    conn.close()
    return databaseOrNone

def formingDatamartWithDefaultServerConnection(datamartName, database):
    load_dotenv()
    return Datamart(
        name = datamartName,
        database=database,
        host=getenv('SYSTEM_DATA_BASE_HOST'),
        port=getenv('SYSTEM_DATA_BASE_PORT'),
        user=getenv('SYSTEM_DATA_BASE_USERNAME'),
        password=getenv('SYSTEM_DATA_BASE_PASSWORD'),
        localdatabase='1'
    )

def getConnectionFromDatamart(datamart):
    return psycopg2.connect(
            database=datamart.database,
            host=datamart.host,
            port=datamart.port,
            user=datamart.user,
            password=datamart.password
        )

def tryCreateDatabaseFromDatamartReturningBoolean(datamart):
    try:
        conn = getDefaultConectionDataMart()
        conn.autocommit = True
        cur = conn.cursor()
        cur.execute('CREATE DATABASE {};'.format(datamart.database))
        cur.close()
        conn.close()
        return True
    except Exception as e:
        print(e)
        return False

def getConnectionFromParameters(database,host,port,user,password):
    return psycopg2.connect(
        database=database,
        host=host,
        port=port,
        user=user,
        password=password
    )

def getDatabaseIfExistsFromParametersConnection(database,host,port,user,password):
    conn = getConnectionFromParameters(database,host,port,user,password)
    cur = conn.cursor()
    cur.execute("SELECT DATNAME FROM pg_database where datname='{}'".format(database))
    databaseOrNone = cur.fetchone()
    cur.close()
    conn.close()
    return databaseOrNone

def formingDatamartWithParameters(name,database,host,port,user,password):
    return Datamart(
        name=name,
        database=database,
        host=host,
        port=port,
        user=user,
        password=password
    )