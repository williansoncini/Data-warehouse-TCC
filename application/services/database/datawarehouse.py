import psycopg2
from dotenv import load_dotenv
from os import getenv


def connectDatawarehouse():
    try:
        load_dotenv()
        conn = psycopg2.connect(
            database=getenv('DW_DATA_BASE_DATABASE'),
            host=getenv('DW_DATA_BASE_HOST'),
            user=getenv('DW_DATA_BASE_USERNAME'),
            password=getenv('DW_DATA_BASE_PASSWORD'),
            port=getenv('DW_DATA_BASE_PORT')
        )

        return conn
    except:
        print('Não foi possível se conectar ao data warehouse')


def importFileinDatawarehouse(table, csvFile):
    load_dotenv()
    conn = psycopg2.connect(
        database=getenv('DW_DATA_BASE_DATABASE'),
        host=getenv('DW_DATA_BASE_HOST'),
        user=getenv('DW_DATA_BASE_USERNAME'),
        password=getenv('DW_DATA_BASE_PASSWORD'),
        port=getenv('DW_DATA_BASE_PORT')
    )
    cur = conn.cursor()
    cur.copy_expert(
        "COPY {} FROM STDOUT WITH CSV HEADER DELIMITER ';'".format(table), csvFile)
    cur.close()
    conn.commit()
    conn.close()


def dropCreateTable(dropCreateTableStatement):
    load_dotenv()
    conn = psycopg2.connect(
        database=getenv('DW_DATA_BASE_DATABASE'),
        host=getenv('DW_DATA_BASE_HOST'),
        user=getenv('DW_DATA_BASE_USERNAME'),
        password=getenv('DW_DATA_BASE_PASSWORD'),
        port=getenv('DW_DATA_BASE_PORT')
    )
    cur = conn.cursor()
    cur.execute(dropCreateTableStatement)
    cur.close()
    conn.commit()
    conn.close()


def dropTableIfExists(tableName):
    load_dotenv()
    conn = psycopg2.connect(
        database=getenv('DW_DATA_BASE_DATABASE'),
        host=getenv('DW_DATA_BASE_HOST'),
        user=getenv('DW_DATA_BASE_USERNAME'),
        password=getenv('DW_DATA_BASE_PASSWORD'),
        port=getenv('DW_DATA_BASE_PORT')
    )
    cur = conn.cursor()
    cur.execute('drop table if exists {}'.format(tableName))
    cur.close()
    conn.commit()
    conn.close()


def getDataFromDatamartTable(tableName):
    load_dotenv()
    conn = psycopg2.connect(
        database=getenv('DW_DATA_BASE_DATABASE'),
        host=getenv('DW_DATA_BASE_HOST'),
        user=getenv('DW_DATA_BASE_USERNAME'),
        password=getenv('DW_DATA_BASE_PASSWORD'),
        port=getenv('DW_DATA_BASE_PORT')
    )
    cur = conn.cursor()
    cur.execute('SELECT * FROM {}'.format(tableName))
    data = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()

    return data


def renameColumnFromTable(tableName, oldColumnName, newColumnName):
    load_dotenv()
    conn = psycopg2.connect(
        database=getenv('DW_DATA_BASE_DATABASE'),
        host=getenv('DW_DATA_BASE_HOST'),
        user=getenv('DW_DATA_BASE_USERNAME'),
        password=getenv('DW_DATA_BASE_PASSWORD'),
        port=getenv('DW_DATA_BASE_PORT')
    )
    cur = conn.cursor()
    cur.execute('ALTER TABLE {} RENAME COLUMN {} TO {};'.format(
        tableName, oldColumnName, newColumnName))
    cur.close()
    conn.commit()
    conn.close()

    return True


def alterTypeFromTable(tableName, columnName, newColumnType):
    load_dotenv()
    conn = psycopg2.connect(
        database=getenv('DW_DATA_BASE_DATABASE'),
        host=getenv('DW_DATA_BASE_HOST'),
        user=getenv('DW_DATA_BASE_USERNAME'),
        password=getenv('DW_DATA_BASE_PASSWORD'),
        port=getenv('DW_DATA_BASE_PORT')
    )
    cur = conn.cursor()
    cur.execute('ALTER TABLE {} ALTER COLUMN {} TYPE {} USING {}::{};'.format(
        tableName, columnName, newColumnType, columnName, newColumnType))
    cur.close()
    conn.commit()
    conn.close()

    return True


def renameTable(oldTableName, newTableName):
    load_dotenv()
    conn = psycopg2.connect(
        database=getenv('DW_DATA_BASE_DATABASE'),
        host=getenv('DW_DATA_BASE_HOST'),
        user=getenv('DW_DATA_BASE_USERNAME'),
        password=getenv('DW_DATA_BASE_PASSWORD'),
        port=getenv('DW_DATA_BASE_PORT')
    )
    cur = conn.cursor()
    cur.execute('ALTER TABLE {} RENAME TO {};'.format(
        oldTableName, newTableName))
    cur.close()
    conn.commit()
    conn.close()

    return True


def checkExistentTable(tableName):
    load_dotenv()
    conn = psycopg2.connect(
        database=getenv('DW_DATA_BASE_DATABASE'),
        host=getenv('DW_DATA_BASE_HOST'),
        user=getenv('DW_DATA_BASE_USERNAME'),
        password=getenv('DW_DATA_BASE_PASSWORD'),
        port=getenv('DW_DATA_BASE_PORT')
    )
    cur = conn.cursor()
    cur.execute(
        "SELECT TABLE_NAME FROM INFORMATION_SCHEMA.TABLES WHERE TABLE_NAME='{}' AND TABLE_SCHEMA='public'".format(tableName))
    data = cur.fetchall()
    cur.close()
    conn.commit()
    conn.close()

    if (data != None):
        return True


def deleteColumnDatamart(tableName, columnName):
    load_dotenv()
    conn = psycopg2.connect(
        database=getenv('DW_DATA_BASE_DATABASE'),
        host=getenv('DW_DATA_BASE_HOST'),
        user=getenv('DW_DATA_BASE_USERNAME'),
        password=getenv('DW_DATA_BASE_PASSWORD'),
        port=getenv('DW_DATA_BASE_PORT')
    )
    cur = conn.cursor()
    cur.execute("ALTER TABLE {} DROP COLUMN IF EXISTS {};".format(
        tableName, columnName))
    cur.close()
    conn.commit()
    conn.close()

    return True


def createTableForEtl(nameTable, columnsAndTypes):
    dropTableStatement = 'DROP TABLE IF EXISTS {};'.format(nameTable)
    createTableStatement = 'CREATE TABLE IF NOT EXISTS {} ('.format(nameTable)
    
    for index, (key, value) in enumerate(columnsAndTypes.items()):
        if index +1 == len(columnsAndTypes):
            createTableStatement += '{} {}'.format(str(key).replace(' ','_'), value)
        else:
            createTableStatement += '{} {},'.format(str(key).replace(' ','_'), value)
    createTableStatement += ');'
    # print(statement)

    load_dotenv()
    conn = psycopg2.connect(
        database=getenv('DW_DATA_BASE_DATABASE'),
        host=getenv('DW_DATA_BASE_HOST'),
        user=getenv('DW_DATA_BASE_USERNAME'),
        password=getenv('DW_DATA_BASE_PASSWORD'),
        port=getenv('DW_DATA_BASE_PORT')
    )
    cur = conn.cursor()
    cur.execute(dropTableStatement)
    conn.commit()
    cur.execute(createTableStatement)
    conn.commit()
    cur.close()
    conn.close()

def importCsvFileInTableWithHeader(filePath, nameTable):
    load_dotenv()
    conn = psycopg2.connect(
        database=getenv('DW_DATA_BASE_DATABASE'),
        host=getenv('DW_DATA_BASE_HOST'),
        user=getenv('DW_DATA_BASE_USERNAME'),
        password=getenv('DW_DATA_BASE_PASSWORD'),
        port=getenv('DW_DATA_BASE_PORT')
    )
    cur = conn.cursor()
    file = open(filePath, 'r')
    cur.copy_expert("COPY {} FROM STDOUT WITH CSV HEADER DELIMITER ';'".format(nameTable),file)
    file.close()
    # cur.copy_from(file,nameTable,sep=';')
    cur.close()
    conn.commit()
    print('conexão sendo fechada!')
    conn.close()  