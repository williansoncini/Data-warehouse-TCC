from django.shortcuts import render,get_list_or_404
from .models import Datamart

# Create your views here.
def datamart_list(request):
    # datamarts = Datamart
    # return render(request,'datamart/list.html',{'datamarts':datamarts})
    return render(request,'application/datamart/list.html')
