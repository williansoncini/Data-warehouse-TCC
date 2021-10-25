from django.views.generic.base import View
from django.shortcuts import redirect, render

class DumpLoad(View):
    def get(self, request):
        return render(request, 'application/input/preUploadOnStagingArea.html')