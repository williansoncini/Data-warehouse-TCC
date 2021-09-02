from application.forms import ColumnStagingAreaForm
from application.services.database.stagingArea import connect
from application.models import ColumnStagingArea,TableStagingArea
from django.shortcuts import get_object_or_404, redirect, render

def showTableDetail(request):
    if request.method == 'GET':
        tableStagingArea = TableStagingArea.objects.get(pk=request.session['pkTableStagingArea'])
        columnsStagingArea = ColumnStagingArea.objects.filter(table=tableStagingArea.id)

        conn = connect()
        cur = conn.cursor()
        cur.execute('SELECT * FROM {}'.format(tableStagingArea.tableName))
        data = cur.fetchall()
        cur.close()
        conn.close()

        return render(request, 'application/input/stagingArea/stagingArea.html',{
            'tableStagingArea':tableStagingArea,
            'columnsStagingArea':columnsStagingArea,
            'data':data
        })

# class StagingAreaView(View):
#     http_method_names = ['get','post','put','delete']

#     def dispatch(self):
#         method = self.request.POST.get('_method','').lower()
#         if method == 'put':
#             self.put(self)

#     def put(self, request, table_id, column_id):
#         print('passei pelo metodo de PUT')        
#         print('vindo da request: ',self.request.method)

def updateColumnStagingArea(request, table_id, column_id):
    if request.method == 'GET':
        columnStagingArea = ColumnStagingArea.objects.get(table_id=table_id, pk=column_id)
        form = ColumnStagingAreaForm(initial={
            'name': columnStagingArea.name,
            'typeColumn':columnStagingArea.typeColumn,
            'typeExpression': columnStagingArea.typeExpression,
            'expression':columnStagingArea.expression
        })
        return render(request, 'application/input/stagingArea/update.html',{
            'form':form
        })
    else:
        columnStagingArea = get_object_or_404(ColumnStagingArea, pk=column_id, table_id=table_id)
        form = ColumnStagingAreaForm(request.POST)
        if form.is_valid():
            columnStagingArea.name = form.cleaned_data['name']
            columnStagingArea.typeColumn = form.cleaned_data['typeColumn']
            columnStagingArea.typeExpression = form.cleaned_data['typeExpression']
            columnStagingArea.expression = form.cleaned_data['expression']

            columnStagingArea.save()
            return redirect('application:stagingArea')
        else:
            return render(request, 'application/input/stagingArea/update.html',{
                'form':form
            })

def deleteColumnStagingArea(request, table_id, column_id):
    if request.method == 'GET':
        columnStagingArea = ColumnStagingArea.objects.get(table_id=table_id, pk=column_id)
        return render(request, 'application/input/stagingArea/delete.html',{
            'columnStagingArea':columnStagingArea
        })
    else:
        columnStagingArea = ColumnStagingArea.objects.get(table_id=table_id, pk=column_id)
        columnStagingArea.delete()
        return redirect('application:stagingArea')
        
def createColumnStagingArea(request, table_id):
    if request.method == 'GET':
        form = ColumnStagingAreaForm()
        return render(request, 'application/input/stagingArea/create.html', {
            'form':form
        })
    else:
        form = ColumnStagingAreaForm(request.POST)
        if form.is_valid():
            columnStagingArea = ColumnStagingArea(
                table_id = table_id,
                name = form.cleaned_data['name'],
                typeColumn = form.cleaned_data['typeColumn'],
                typeExpression = form.cleaned_data['typeExpression'],
                expression = form.cleaned_data['expression']
            )
            columnStagingArea.save()

            return redirect('application:stagingArea')
            
