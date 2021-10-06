from django.http.response import HttpResponse
from application.forms import ColumnStagingAreaForm
from application.services.database.stagingArea import connect, makeSelectStatement, makeStatementCreateTable
from application.models import ColumnStagingArea,TableStagingArea
from django.shortcuts import get_object_or_404, redirect, render

def StagingAreaDetail(request):
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
    else:
        tableStagingArea = TableStagingArea.objects.get(pk=request.session['pkTableStagingArea'])
        columnsStagingArea = ColumnStagingArea.objects.filter(table=tableStagingArea.id)
        newTableName = request.POST.get('tableName','')

        if tableStagingArea.tableName != newTableName:
            conn = connect()
            cur = conn.cursor()
            cur.execute('ALTER TABLE IF EXISTS {} RENAME TO {};'.format(tableStagingArea.tableName,newTableName))
            cur.close()
            conn.commit()
            conn.close()

        tableStagingArea.tableName = newTableName
        tableStagingArea.statementCreateTable = makeStatementCreateTable(newTableName, columnsStagingArea)
        tableStagingArea.statementSelect = makeSelectStatement(newTableName, columnsStagingArea)
        tableStagingArea.save()
        
        return redirect('application:stagingArea-statement')

def createColumnStagingArea(request, table_id):
    if request.method == 'GET':
        return render(request, 'application/input/stagingArea/column/create.html')
    else:
        tableStagingArea = TableStagingArea.objects.get(pk=table_id)

        columnStagingArea = ColumnStagingArea(
            table_id = table_id,
            name = request.POST.get('columnName'),
            typeColumn = request.POST.get('columnType')
        )
        columnStagingArea.save()

        conn = connect()
        cur = conn.cursor()
        cur.execute('ALTER TABLE IF EXISTS {} ADD COLUMN {} {};'.format(tableStagingArea.tableName,
            columnStagingArea.name,
            columnStagingArea.typeColumn
        ))
        cur.close()
        conn.commit()
        conn.close()

        return redirect('application:stagingArea')

def updateColumnStagingArea(request, table_id, column_id):
    if request.method == 'GET':
        columnStagingArea = ColumnStagingArea.objects.get(table_id=table_id, pk=column_id)

        return render(request, 'application/input/stagingArea/column/update.html',{
            'columnName':columnStagingArea.name,
            'columnType': columnStagingArea.typeColumn
        })
    else:
        columnStagingArea = get_object_or_404(ColumnStagingArea, pk=column_id, table_id=table_id)
        tableStagingArea = TableStagingArea.objects.get(pk=table_id)
        
        newColumnName = request.POST.get('columnName')
        newColumnType = request.POST.get('columnType')

        if newColumnName != columnStagingArea.name:
            conn = connect()
            cur = conn.cursor()
            cur.execute("ALTER TABLE IF EXISTS {} RENAME COLUMN {} TO {};".format(tableStagingArea.tableName,
                columnStagingArea.name,
                newColumnName
            ))
            cur.close()
            conn.commit()
            conn.close()

            columnStagingArea.name = newColumnName
            columnStagingArea.save()

        print('tipo novo: ', newColumnType)
        print('tipo antigo: ', columnStagingArea.typeColumn)
        if newColumnType != columnStagingArea.typeColumn:
            try:
                conn = connect()
                cur = conn.cursor()
                cur.execute("ALTER TABLE IF EXISTS {} ALTER COLUMN {} TYPE {} USING {}::{};".format(tableStagingArea.tableName,
                    columnStagingArea.name,
                    newColumnType,
                    columnStagingArea.name,
                    newColumnType
                    ))
                print("ALTER TABLE IF EXISTS {} ALTER COLUMN {} TYPE {} USING {}::{};".format(tableStagingArea.tableName,
                    columnStagingArea.name,
                    columnStagingArea.typeColumn,
                    columnStagingArea.name,
                    columnStagingArea.typeColumn
                    ))

                cur.close()
                conn.commit()
                conn.close()
         
                columnStagingArea.typeColumn = newColumnType
                columnStagingArea.save()
            except:
                print('Tipo de dados não suportado pela coluna')

        return redirect('application:stagingArea')

def deleteColumnStagingArea(request, table_id, column_id):
    if request.method == 'GET':
        columnStagingArea = ColumnStagingArea.objects.get(table_id=table_id, pk=column_id)
        return render(request, 'application/input/stagingArea/column/delete.html',{
            'columnStagingArea':columnStagingArea
        })
    else:
        tableStagingArea = TableStagingArea.objects.get(pk=table_id)
        columnStagingArea = ColumnStagingArea.objects.get(table_id=table_id, pk=column_id)

        conn = connect()
        cur = conn.cursor()
        cur.execute("ALTER TABLE IF EXISTS {} DROP COLUMN {};".format(tableStagingArea.tableName,
        columnStagingArea.name))
        cur.close()
        conn.commit()
        conn.close()
        
        columnStagingArea.delete()
        return redirect('application:stagingArea')
        
def deleteTableStagingArea(request, table_id):
    tableStagingArea = TableStagingArea.objects.get(pk=table_id)

    conn = connect()
    cur = conn.cursor()
    cur.execute("DROP TABLE IF EXISTS {};".format(tableStagingArea.tableName))
    cur.close()
    conn.commit()
    conn.close()

    tableStagingArea.delete()

    return redirect ('application:home')

def statementView(request):
    if request.method == 'GET':
        tableStagingArea = TableStagingArea.objects.get(pk=request.session['pkTableStagingArea'])
        
        print(tableStagingArea.statementCreateTable)

        return render(request,'application/input/stagingArea/statement.html',{
            'statementCreateTable': tableStagingArea.statementCreateTable,
            'statementSelect': tableStagingArea.statementSelect
        })
    else:
        tableStagingArea = TableStagingArea.objects.get(pk=request.session['pkTableStagingArea'])
        tableStagingArea.statementCreateTable = request.POST.get('statementCreateTable','')
        tableStagingArea.statementSelect = request.POST.get('statementSelect','')
        tableStagingArea.save()



        return HttpResponse('sucess!')
        