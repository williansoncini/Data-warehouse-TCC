from application.services.database.datamart import dropCreateTable, importFileInDatamart
from application.services.database.stagingArea import clearStagingArea, connect, makeSelectStatement, makeStatementCreateTable
from application.models import ColumnDataMart, ColumnStagingArea, Datamart, TableDataMart,TableStagingArea
from django.shortcuts import get_object_or_404, redirect, render
from os import path
from application.services.database.stagingArea import exportSelectToCsv

def StagingAreaDetail(request):
    if request.method == 'GET':
        createTableAutomatically = request.session['createTableAutomatically']
        tableStagingArea = TableStagingArea.objects.get(pk=request.session['pkTableStagingArea'])
        columnsStagingArea = ColumnStagingArea.objects.filter(table=tableStagingArea.id)

        conn = connect()
        cur = conn.cursor()
        cur.execute('SELECT * FROM {}'.format(tableStagingArea.tableName))
        data = cur.fetchall()
        cur.close()
        conn.close()

        datamartDestiny = request.session['datamartSelected']

        return render(request, 'application/stagingArea/stagingArea.html',{
            'tableStagingArea':tableStagingArea,
            'columnsStagingArea':columnsStagingArea,
            'data':data,
            'datamartDestiny': datamartDestiny,
            'createTableAutomatically': createTableAutomatically
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
        return render(request, 'application/stagingArea/column/create.html')
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
            columnStagingArea.type
        ))
        cur.close()
        conn.commit()
        conn.close()

        return redirect('application:stagingArea')

def updateColumnStagingArea(request, table_id, column_id):
    if request.method == 'GET':
        columnStagingArea = ColumnStagingArea.objects.get(table_id=table_id, pk=column_id)

        return render(request, 'application/stagingArea/column/update.html',{
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
        print('tipo antigo: ', columnStagingArea.type)
        if newColumnType != columnStagingArea.type:
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
                    columnStagingArea.type,
                    columnStagingArea.name,
                    columnStagingArea.type
                    ))

                cur.close()
                conn.commit()
                conn.close()
         
                columnStagingArea.type = newColumnType
                columnStagingArea.save()
            except:
                print('Tipo de dados não suportado pela coluna')

        return redirect('application:stagingArea')

def deleteColumnStagingArea(request, table_id, column_id):
    if request.method == 'GET':
        columnStagingArea = ColumnStagingArea.objects.get(table_id=table_id, pk=column_id)
        return render(request, 'application/stagingArea/column/delete.html',{
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
    createTableAutomatically = request.session['createTableAutomatically']
    tableStagingArea = TableStagingArea.objects.get(pk=request.session['pkTableStagingArea'])
    
    if request.method == 'GET':
        return render(request,'application/stagingArea/statement.html',{
            'statementCreateTable': tableStagingArea.statementCreateTable,
            'statementSelect': tableStagingArea.statementSelect,
            'createTableAutomatically':createTableAutomatically
        })
    else:
        tableStagingArea.statementCreateTable = request.POST.get('statementCreateTable','')
        tableStagingArea.statementSelect = request.POST.get('statementSelect','')
        tableStagingArea.save()

        #gerar o arquivo CSV
        with open(path.dirname(__file__) + '/../../../exports/teste1.csv', 'w+') as csvFile:
            exportSelectToCsv(tableStagingArea.statementSelect, csvFile)
            datamart = Datamart.objects.get(name=request.session['datamartSelected'])
            datamart.database = str(datamart.database).lower()
            print(datamart)
            
            dropCreateTableStatement = str(tableStagingArea.statementCreateTable)
            dropCreateTableStatement = dropCreateTableStatement.strip()
            tableName = str(tableStagingArea.tableName).lower()

            if(createTableAutomatically):
                dropCreateTable(datamart,dropCreateTableStatement)
        
        file = open(path.dirname(__file__) + '/../../../exports/teste1.csv', 'r')
        importFileInDatamart(datamart,tableName,file)
        file.close()

        (tableDatamart,__) = TableDataMart.objects.get_or_create(
            datamart=datamart,
            name=tableStagingArea.tableName
        )
        tableDatamart.save()

        columnStagingArea = ColumnStagingArea.objects.filter(table_id=tableStagingArea.id)
        for column in columnStagingArea:
            (newColumnDatamart,__) = ColumnDataMart.objects.get_or_create(
                table=tableDatamart,
                name=column.name,
                type=column.typeColumn
            )
            newColumnDatamart.save()
        
        #limpar StagingArea
        clearStagingArea(tableName)
        columnStagingArea.delete()
        tableStagingArea.delete()

        return redirect('application:home')
        # return HttpResponse('sucess!')
        
    