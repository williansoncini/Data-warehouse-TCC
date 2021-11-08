from django.views import View
from django.shortcuts import render, redirect

from application.models import CubeDatawarehouse

class ListCubes(View):
    def get(self, request):
        cubes = CubeDatawarehouse.objects.all()

        return render(request, 'application/datawarehouse/cubes/listCubes.html',{
            'cubes':cubes
        })
