from os import getenv
from django.contrib import messages
from django.http.response import HttpResponse
from django.shortcuts import redirect, render
from django.views import View
from dotenv.main import load_dotenv
import psycopg2

from application.models import ExtractConnection

class ExtractConnectionDeleteView(View):
    def get(self, request, extractConnection_id):
        extractConnection = ExtractConnection.objects.get(pk=extractConnection_id)
        return render(request, 'application/input/extractConnections/extractConnectionsDelete.html',{
            'extractConnection':extractConnection
        }) 

    def post(self, request, extractConnection_id):
        extractConnection = ExtractConnection.objects.get(pk=extractConnection_id)
        try:
            extractConnection.delete()
            messages.success(request, 'Connection as been deleted!')
            return redirect('application:extract-connections')
        except:
            messages.warning(request, 'Fail to delete!')
            return redirect('application:extract-connections-delete', extractConnection_id=extractConnection_id)
