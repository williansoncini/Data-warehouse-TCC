import psycopg2
from dotenv import load_dotenv
from os import getenv

def connectInDatamartWithParameters(database, host, user, password, port):
    try:
        return psycopg2.connect(
        database=database,
        host=host,
        port=port,
        user=user,
        password=password
    )
    except Exception as e:
        print(e)
        print('não foi possível se conectar ao banco de dados')

def connectLocalDatamart():
    try:    
        load_dotenv()
        conn = psycopg2.connect(
            database=getenv('STAGING_AREA_DATABASE'),
            host=getenv('STAGING_AREA_HOST'),
            user=getenv('STAGING_AREA_USERNAME'),
            password=getenv('STAGING_AREA_PASSWORD'),
            post=getenv('STAGING_AREA_PORT')
        )

        return conn
    except:
        print('Não foi possível se conectar ao banco de dados')
    
def importFileInDatamart(datamart, tableDatamart, csvFile):
    conn = psycopg2.connect(
        database= datamart.database,
        host=datamart.host,
        user=datamart.user,
        password=datamart.password,
        port=datamart.port
    )
    cur = conn.cursor()
    # cur.copy_from(csvFile,tableDatamart,sep=';')
    cur.copy_expert("COPY {} FROM STDOUT WITH CSV HEADER DELIMITER ';'".format(tableDatamart),csvFile)
    # cur.execute('select * from {}'.format())
    cur.close()
    conn.commit()
    conn.close()

def dropCreateTable(datamart, dropCreateTableStatement):
    conn = psycopg2.connect(
        database= datamart.database,
        host=datamart.host,
        user=datamart.user,
        password=datamart.password,
        port=datamart.port
    )
    cur = conn.cursor()
    cur.execute(dropCreateTableStatement)
    cur.close()
    conn.commit()
    conn.close()
   
def dropTableIfExists(datamart, tableName):
    conn = psycopg2.connect(
        database= datamart.database,
        host=datamart.host,
        user=datamart.user,
        password=datamart.password,
        port=datamart.port
    )
    cur = conn.cursor()
    cur.execute('drop table if exists {}'.format(tableName))
    cur.close()
    conn.commit()
    conn.close()

def getDataFromDatamartTable(datamart, datamartTableName):
        database = datamart.database
        host = datamart.host
        user = datamart.user
        password = datamart.password
        port = datamart.port

        conn = connectInDatamartWithParameters(database, host, user, password, port)
        cur = conn.cursor()
        cur.execute('SELECT * FROM {}'.format(datamartTableName))
        data = cur.fetchall()
        cur.close()
        conn.commit()
        conn.close()

        return data

def renameColumnFromTable(datamart, tableName, oldColumnName, newColumnName):
    database = datamart.database
    host = datamart.host
    user = datamart.user
    password = datamart.password
    port = datamart.port

    conn = connectInDatamartWithParameters(database, host, user, password, port)
    cur = conn.cursor()
    cur.execute('ALTER TABLE {} RENAME COLUMN {} TO {};'.format(tableName, oldColumnName, newColumnName))
    cur.close()
    conn.commit()
    conn.close()

    return True

def alterTypeFromTable(datamart, tableName, columnName, newColumnType):
    database = datamart.database
    host = datamart.host
    user = datamart.user
    password = datamart.password
    port = datamart.port

    conn = connectInDatamartWithParameters(database, host, user, password, port)
    cur = conn.cursor()
    cur.execute('ALTER TABLE {} ALTER COLUMN {} TYPE {} USING {}::{};'.format(tableName, columnName, newColumnType,columnName,newColumnType))
    cur.close()
    conn.commit()
    conn.close()

    return True
