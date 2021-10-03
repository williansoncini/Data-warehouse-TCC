from os import getenv
from django.contrib import messages
from django.http.response import HttpResponse, JsonResponse
from dotenv.main import load_dotenv
import psycopg2
from application.models import Datamart
from django.shortcuts import redirect, render
from django.views import View

class DatamartDelete(View):
    def get(self, request, datamart_id):
        datamart = Datamart.objects.get(pk=datamart_id) 
        # datamartConnection = DatamartConnection.objects.get(datamart_id=datamart_id)
        return render(request, 'application/datamart/delete.html', {
            'datamart' : datamart
            # 'connection': datamartConnection
        })

    def post(self, request, datamart_id):
        datamart = Datamart.objects.get(pk=datamart_id)
        # datamartConnection = DatamartConnection.objects.get(datamart_id=datamart_id)

        if datamart.localdatabase:
            try:
                conn = getDefaultConectionDataMart()
                conn.autocommit = True
                cur = conn.cursor()
                cur.execute("SELECT DATNAME FROM pg_database where datname='{}'".format(datamart.database))
                databaseExistent = cur.fetchone()
                
                if databaseExistent != None:
                    cur.execute('DROP DATABASE {};'.format(datamart.database))
                    datamart.delete()
                    datamart.delete()   
                    # messages.success(request,'teste')
                    return redirect('application:datamart-list')
                else:
                    return render(request, 'application/datamart/delete.html', {
                        'datamart' : datamart
                        # 'connection': datamartConnection
                    })
            except Exception as e:
                print(e)
                return redirect('application:datamart-list')
        else:  
            datamart.delete()
            # datamartConnection.delete()

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