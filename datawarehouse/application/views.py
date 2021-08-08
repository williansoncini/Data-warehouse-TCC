from django.http.response import HttpResponse, HttpResponseRedirect
from django.shortcuts import render,get_list_or_404
from .models import Datamart
from .forms import fileForm
from .services.file.fileService import handle_uploaded_file
from django.contrib import messages

# Create your views here.
def datamart_list(request):
    # datamarts = Datamart
    # return render(request,'datamart/list.html',{'datamarts':datamarts})
    return render(request,'application/datamart/list.html')

def fileinput(request):
    if request.method == 'POST':
        file = fileForm(request.POST, request.FILES)
        if file.is_valid():
            handle_uploaded_file(request.FILES['file']) 
            messages.success(request,'Formulario submetido com sucesso')
    else:
        file = fileForm()

    return render(request,'application/file/inputfile.html', {'form':file})