from django.shortcuts import render

def getHome(request):
    request.session['tempFilePk'] = ''
    request.session['createTableAutomatically'] = ''
    request.session['pkTableStagingArea'] = ''
    request.session['tableSelected'] = ''
    request.session['datamartSelected'] = ''
    request.session['choiceInput'] = ''
    request.session['tableDatamart-id-create-table-datamart'] = ''
    request.session['datawarehouse-datamartSelected'] = ''
    request.session['createTableAutomatically'] = ''
    request.session['createTableAutomatically'] = ''
    request.session['createTableAutomatically'] = ''
    request.session['createTableAutomatically'] = ''
    request.session['createTableAutomatically'] = ''
    request.session['createTableAutomatically'] = ''


    return render(request, 'application/home.html')