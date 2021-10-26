from os import getenv
from django.contrib import messages
from dotenv.main import load_dotenv
import psycopg2
from application.models import Datamart
from django.shortcuts import redirect, render
from django.views import View

class DatamartUpdate(View):
    def get(self, request, datamart_id):
        datamart = Datamart.objects.get(pk=datamart_id) 
        return render(request, 'application/datamart/update.html', {
            'datamart' : datamart
        })

    def post(self, request, datamart_id):
        datamart = Datamart.objects.get(pk=datamart_id)

        datamartName=request.POST.get('datamart-name','')
        database=request.POST.get('datamart-databaseName','')
        host = request.POST.get('datamart-host','')
        port = request.POST.get('datamart-port','')
        user = request.POST.get('datamart-username')
        password = request.POST.get('datamart-password')
        oldDatabaseName = datamart.database

        if datamart.name != datamartName:
            datamart.name = datamartName
        
        if datamart.host != host:
            datamart.host = host

        if datamart.port != port:
            datamart.port = port

        if datamart.user != user:
            datamart.user = user

        if datamart.password != password:
            datamart.password = password

        if datamart.database != database:
            if datamart.localdatabase:
                datamart.database = database
                try:
                    oldDatabaseExistentsOrNone = checkIfDatabaseExistsForChaging(oldDatabaseName)
                    if oldDatabaseExistentsOrNone != None:
                        changedNameForDatabaseBoolean =  tryMakeRenameDatabaseWithDefaultServerConnectionReturningBool(oldDatabaseName, database)
                        if changedNameForDatabaseBoolean :
                            datamart.save()
                            return redirect('application:datamart-list')
                        else:
                            return render(request, 'application/datamart/update.html', {
                                'datamart' : datamart
                            })
                except Exception as e:
                    print(e)
                    return redirect('application:datamart-list')
        else:
            connectionBoolean = tryConnectionFromParametersReturningBool(database,host,port,user,password)
            if connectionBoolean:
                datamart.save()
                return redirect('application:datamart-list')
            else:
                return render(request, 'application/datamart/update.html', {
                    'datamart' : datamart
                })       

def getDefaultConectionDataMart():
    load_dotenv()
    return psycopg2.connect(
        database=getenv('SYSTEM_DATA_BASE_DATABASE'),
        host=getenv('SYSTEM_DATA_BASE_HOST'),
        port=getenv('SYSTEM_DATA_BASE_PORT'),
        user=getenv('SYSTEM_DATA_BASE_USERNAME'),
        password=getenv('SYSTEM_DATA_BASE_PASSWORD')
    )

def checkIfDatabaseExistsForChaging(database):
    conn = getDefaultConectionDataMart()
    cur = conn.cursor()
    cur.execute("SELECT DATNAME FROM pg_database where datname='{}'".format(database))
    databaseOrNone = cur.fetchone()
    return databaseOrNone

def tryMakeRenameDatabaseWithDefaultServerConnectionReturningBool(oldDatabaseName, newDatabaseName):
    conn = getDefaultConectionDataMart()
    conn.autocommit = True
    cur = conn.cursor()
    cur.execute("alter database {} rename to {}".format(oldDatabaseName, newDatabaseName))
    cur.execute("SELECT DATNAME FROM pg_database where datname='{}'".format(newDatabaseName))
    newDatabaseExistents = cur.fetchone()
    cur.close()
    conn.close()
    if newDatabaseExistents != None:
        return True
    else:
        return False

def getConnectionFromParameters(database,host,port,user,password):
    return psycopg2.connect(
        database=database,
        host=host,
        port=port,
        user=user,
        password=password
    )

def tryConnectionFromParametersReturningBool(database,host,port,user,password):
    conn = getConnectionFromParameters(database,host,port,user,password)
    cur = conn.cursor()
    cur.execute("SELECT DATNAME FROM pg_database where datname='{}'".format(database))
    databaseExists = cur.fetchone()
    cur.close()
    conn.close()
    if databaseExists != None:
        return True
    else:
        return False
