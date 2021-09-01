from application.forms import ExpressionStagingAreaForm
from application.services.database.stagingArea import connect
from application.models import ColumnStagingArea, ExpressionColumnStagingArea, TableStagingArea
from django.shortcuts import render

def showTableDetail(request):
    if request.method == 'GET':
        tableStagingArea = TableStagingArea.objects.get(pk=request.session['pkTableStagingArea'])
        columnsStagingArea = ColumnStagingArea.objects.filter(table=tableStagingArea.id)

        dictionarieWithColumnsAndTypes = {}
        listColumns=[]
        for column in columnsStagingArea:
            dictionarieWithColumnsAndTypes[column.name] = column.typeColumn
            listColumns.append(column.name)
        
        conn = connect()
        cur = conn.cursor()
        cur.execute('SELECT * FROM {}'.format(tableStagingArea.tableName))
        data = cur.fetchall()
        cur.close()
        conn.close()

        expressionForms = []
        expressionsColumnsStagingArea = ExpressionColumnStagingArea.objects.filter(table=tableStagingArea.id)
        for expression in expressionsColumnsStagingArea:
            form = ExpressionStagingAreaForm()
            form.table = expression.table
            form.column = expression.column
            form.expression = expression.expression
            expressionForms.append(form)            

        return render(request, 'application/input/stagingArea.html',{
            'nameTable':tableStagingArea.tableName,
            'dictionarieWithColumnsAndTypes':dictionarieWithColumnsAndTypes,
            'listColumns': listColumns,
            'data':data,
            'expressionForms': expressionForms
        })

def modal(request):
    print('***************************passei')
    return render(request, 'application/input/modal.html')

