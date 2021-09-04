from django.http.response import HttpResponse
from application.forms import ColumnStagingAreaForm
from application.services.database.stagingArea import connect, makeSelectStatement, makeStatementCreateTable
from application.models import ColumnStagingArea,TableStagingArea
from django.shortcuts import get_object_or_404, redirect, render

def showTableDetail(request):
    if request.method == 'GET':
        tableStagingArea = TableStagingArea.objects.get(pk=request.session['pkTableStagingArea'])
        columnsStagingArea = ColumnStagingArea.objects.filter(table=tableStagingArea.id)

        statementCreateTable = makeStatementCreateTable(tableStagingArea.tableName, columnsStagingArea)
        statementSelect = makeSelectStatement(tableStagingArea.tableName, columnsStagingArea)

        conn = connect()
        cur = conn.cursor()
        cur.execute('SELECT * FROM {}'.format(tableStagingArea.tableName))
        data = cur.fetchall()
        cur.close()
        conn.close()

        return render(request, 'application/input/stagingArea/stagingArea.html',{
            'tableStagingArea':tableStagingArea,
            'columnsStagingArea':columnsStagingArea,
            'data':data,
            'statementSelect':statementSelect,
            'statementCreateTable':statementCreateTable
        })
    else:
        tableStagingArea = TableStagingArea.objects.get(pk=request.session['pkTableStagingArea'])
        columnsStagingArea = ColumnStagingArea.objects.filter(table=tableStagingArea.id)

        tableStagingArea.statementCreateTable = makeStatementCreateTable(tableStagingArea.tableName, columnsStagingArea)
        tableStagingArea.statementSelect = makeSelectStatement(tableStagingArea.tableName, columnsStagingArea)
        tableStagingArea.save()
        
        return HttpResponse('sucess')

def updateColumnStagingArea(request, table_id, column_id):
    if request.method == 'GET':
        columnStagingArea = ColumnStagingArea.objects.get(table_id=table_id, pk=column_id)
        form = ColumnStagingAreaForm(initial={
            'name': columnStagingArea.name,
            'typeColumn':columnStagingArea.typeColumn
        })
        return render(request, 'application/input/stagingArea/column/update.html',{
            'form':form
        })
    else:
        columnStagingArea = get_object_or_404(ColumnStagingArea, pk=column_id, table_id=table_id)
        form = ColumnStagingAreaForm(request.POST)
        if form.is_valid():
            columnStagingArea.name = form.cleaned_data['name']
            columnStagingArea.typeColumn = form.cleaned_data['typeColumn']

            columnStagingArea.save()
            return redirect('application:stagingArea')
        else:
            return render(request, 'application/input/stagingArea/column/update.html',{
                'form':form
            })

def deleteColumnStagingArea(request, table_id, column_id):
    if request.method == 'GET':
        columnStagingArea = ColumnStagingArea.objects.get(table_id=table_id, pk=column_id)
        return render(request, 'application/input/stagingArea/column/delete.html',{
            'columnStagingArea':columnStagingArea
        })
    else:
        columnStagingArea = ColumnStagingArea.objects.get(table_id=table_id, pk=column_id)
        columnStagingArea.delete()
        return redirect('application:stagingArea')
        
def createColumnStagingArea(request, table_id):
    if request.method == 'GET':
        form = ColumnStagingAreaForm()
        return render(request, 'application/input/stagingArea/column/create.html', {
            'form':form
        })
    else:
        form = ColumnStagingAreaForm(request.POST)
        if form.is_valid():
            columnStagingArea = ColumnStagingArea(
                table_id = table_id,
                name = form.cleaned_data['name'],
                typeColumn = form.cleaned_data['typeColumn']
            )
            columnStagingArea.save()

            return redirect('application:stagingArea')
