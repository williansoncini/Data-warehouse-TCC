# from application.forms import ExpressionStagingAreaForm
from application.services.database.stagingArea import connect
from application.models import ColumnStagingArea,TableStagingArea
from django.shortcuts import render

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

        return render(request, 'application/input/stagingArea.html',{
            'nameTable':tableStagingArea.tableName,
            'columnsStagingArea':columnsStagingArea,
            # 'dictionarieWithColumnsAndTypes':dictionarieWithColumnsAndTypes,
            # 'listColumns': listColumns,
            'data':data
            # 'expressionsColumnsStagingArea': expressionsColumnsStagingArea,
            # 'expressionForm': expressionForm
        })

def addExpression(request, table_id, column_id):
    print(table_id)
    print(column_id)
    return render(request, 'application/input/expression.html')


