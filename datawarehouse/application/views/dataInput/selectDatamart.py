from django.shortcuts import render
from django.views.generic.base import View

from application.models import Datamart

class SelectDatamart(View):

    def get(self, request):
        datamarts = Datamart.objects.all()

        return render(request, 'application/input/selectDatamart.html/', {
            'datamarts': datamarts
        })

    def post(self, request):
        pass


