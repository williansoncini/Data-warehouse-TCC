from django.contrib import messages
from django.views import View
from django.shortcuts import redirect, render

from application.models import ColumnDataMart, Datamart, TableDataMart
from application.services.database.datamart import connectInDatamartWithParameters
from application.services.database.stagingArea import connect

class TableDatamartCreateView(View):
    def get(self, request, table_id):
        tableDatamart = TableDataMart.objects.get(pk=table_id)
        columnsDatamart = ColumnDataMart.objects.filter(table=tableDatamart)
        print('create table datamart')
        return render(request, 'application/datamart/tables/create.html',{
            'tableDatamart':tableDatamart,
            'columnsDatamart':columnsDatamart
        })

    def post(self, request, table_id):
        tableDatamart = TableDataMart.objects.get(pk=table_id)
        columnsDatamart = ColumnDataMart.objects.filter(table=tableDatamart)
        datamart = Datamart.objects.get(pk=tableDatamart.datamart.id)

        for column in columnsDatamart:
            print(column.id)

        statementCreateTable = self.makeStatementCreateTableForDatamart(tableDatamart.name, columnsDatamart)
        statementCreateTable = statementCreateTable.strip()

        tableCreated = self.createTableInDatamart(statementCreateTable,datamart)
        if (tableCreated):
            messages.success(request,"Table '{}' create sucessful at datamart '{}'!".format(tableDatamart.name, datamart.name))
            return redirect('application:datamart-tables')
        else:            
            messages.warning(request, "Error at create table '{}' at datamart '{}'".format(tableDatamart.name, datamart.name))
            return render(request, 'application/datamart/tables/create.html',{
                'tableDatamart':tableDatamart,
                'columnsDatamart':columnsDatamart
            })

    def makeStatementCreateTableForDatamart(self, tableName, Columns):
        statement = 'DROP TABLE IF EXISTS {};\n'.format(tableName)
        statement += 'CREATE TABLE IF NOT EXISTS {} ('.format(tableName)

        lenColumns = len(Columns)
        for index, column in enumerate(Columns):
            if index +1 == lenColumns:
                statement += '{} {}'.format(column.name, column.type)
            else:
                statement += '{} {},'.format(column.name, column.type)
        statement += ');'

        return statement

    def createTableInDatamart(self, statementCreateTable, datamart):
        database = datamart.database
        host = datamart.host
        user = datamart.user
        password = datamart.password
        port = datamart.port

        conn = connectInDatamartWithParameters(database, host, user, password, port)
        cur = conn.cursor()
        cur.execute(statementCreateTable)
        cur.close()
        conn.commit()
        conn.close()

        return True
