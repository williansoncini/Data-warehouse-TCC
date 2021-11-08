from django.views import View
from django.shortcuts import render, redirect
from application.models import TableDatawarehouse
from django.contrib import messages


class SelectTablesForCube(View):
    def get(self, request):
        tables = TableDatawarehouse.objects.all()

        return render (request, 'application/datawarehouse/cubes/create/selectTables.html', {
            'tables': tables
        })

    def post(self, request):
        factTable = request.POST.get('fact')
        firstDimension = request.POST.get('first-dimension')
        secondDimension = request.POST.get('second-dimension')
        thirdDimension = request.POST.get('third-dimension')
        fourthDimension = request.POST.get('fourth-dimension')

        duplicateValues = []
        array = [factTable,firstDimension,secondDimension,thirdDimension,fourthDimension]
        for i in range(0,len(array)):
            for j in range(i+1, len(array)):
                if (array[i] == array[j]):
                    duplicateValues.append(array[j])

        if len(duplicateValues) != 0:
            messages.warning(request, 'Duplicate values: {}'.format(duplicateValues))
            return redirect('application:datawarehouse-cubes-select-tables')    

        request.session['factTable'] = factTable
        request.session['firstDimension'] = firstDimension
        request.session['secondDimension'] = secondDimension
        request.session['thirdDimension'] = thirdDimension
        request.session['fourthDimension'] = fourthDimension
        return redirect('application:datawarehouse-cubes-select-tables-cubes')