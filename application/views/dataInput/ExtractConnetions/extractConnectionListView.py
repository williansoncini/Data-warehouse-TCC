from django.views import View
from django.shortcuts import render
from application.models import ExtractConnection

class ExtractConnectionsListView(View):
    def get(self, request):
        extractConnections = ExtractConnection.objects.all()
        return render(request, 'application/input/extractConnections/extractConnectionsList.html',{
            'extractConnections':extractConnections
        })
