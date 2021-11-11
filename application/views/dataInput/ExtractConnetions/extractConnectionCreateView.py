from os import getenv
from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from dotenv.main import load_dotenv
import psycopg2

from application.models import ExtractConnection

class ExtractConnectionCreateView(View):
    def get(self, request):
        return render(request, 'application/input/extractConnections/extractConnectionsCreate.html') 

    def post(self, request):
        name = request.POST.get('name')

        existsConnection = ExtractConnection.objects.filter(name=name).first()

        if existsConnection != None:
            messages.warning(request, "Connect '{}' already exists".format(name))

        serverConnection = bool(request.POST.get('server-connection',''))
        databaseName = request.POST.get('databaseName')

        if serverConnection:
            load_dotenv()
            try:
                conn = psycopg2.connect(
                    host=getenv('SYSTEM_DATA_BASE_HOST'),
                    database=databaseName,
                    user=getenv('SYSTEM_DATA_BASE_USERNAME'),
                    password=getenv('SYSTEM_DATA_BASE_PASSWORD')
                )
                conn.close()
            except Exception as e:
                print(e)
                messages.warning(request, 'Falha ao se conectar!')
                return redirect('application:extract-connections-create')

            ExtractConnection(
                name = name,
                host=getenv('SYSTEM_DATA_BASE_HOST'),
                database=databaseName,
                user=getenv('SYSTEM_DATA_BASE_USERNAME'),
                password=getenv('SYSTEM_DATA_BASE_PASSWORD'),
                port = getenv('SYSTEM_DATA_BASE_PORT'),
                localdatabase = '1'
            ).save()
            messages.success(request,"Connection '{}' created successfully!".format(name))
            return redirect('application:extract-connections')
        else:    
            host = request.POST.get('host')
            username = request.POST.get('username')
            password = request.POST.get('password')
            port = request.POST.get('port')
            print(databaseName)
            print(host)
            print(username)
            print(password)
            print(port)
            try:
                conn = psycopg2.connect(
                    host=host,
                    database=databaseName,
                    user=username,
                    password=password,
                    port=port
                )
                conn.close()
            except Exception as e:
                print(e)
                messages.warning(request, 'Falha ao se conectar!')
                return redirect('application:extract-connections-create')

            ExtractConnection(
                name = name,
                host=host,
                database=databaseName,
                user=username,
                password=password,
                port=port
            ).save()
            messages.success(request,"Connection '{}' created successfully!".format(name))
            return redirect('application:extract-connections')
