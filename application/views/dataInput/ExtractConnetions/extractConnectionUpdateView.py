from os import getenv
from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from dotenv.main import load_dotenv
import psycopg2

from application.models import ExtractConnection

class ExtractConnectionUpdateView(View):
    def get(self, request, extractConnection_id):
        extractConnection = ExtractConnection.objects.get(pk=extractConnection_id)
        return render(request, 'application/input/extractConnections/extractConnectionsUpdate.html',{
            'extractConnection':extractConnection
        }) 

    def post(self, request, extractConnection_id):
        name = request.POST.get('name')
        database = request.POST.get('databaseName')
        host = request.POST.get('host')
        port = request.POST.get('port')
        user = request.POST.get('username')
        password = request.POST.get('password')

        extractConnection = ExtractConnection.objects.get(pk=extractConnection_id)

        if name != extractConnection.name:
            extractConnection.name = name

        if database != extractConnection.database:
            extractConnection.database = database

        if host != extractConnection.host:
            extractConnection.host = host

        if port != extractConnection.port:
            extractConnection.port = port

        if user != extractConnection.user:
            extractConnection.user = user

        if password != extractConnection.password:
            extractConnection.password = password

        try:
            conn = psycopg2.connect(
                host=extractConnection.host,
                database=extractConnection.database,
                user=extractConnection.user,
                password=extractConnection.password
            )
            conn.close()
            extractConnection.save()
            messages.success(request, 'Extract Connection updated!')
            return redirect('application:extract-connections')
        except:
            messages.warning(request, 'Fail to connect! Try again!')
            return redirect('application:extract-connections-update', extractConnection_id=extractConnection_id)
