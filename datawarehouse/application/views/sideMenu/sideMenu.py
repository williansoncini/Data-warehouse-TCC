from django.shortcuts import render

def getMenuInput(request):

    return render(request, 'application/input/menu.html')