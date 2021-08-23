import psycopg2

def connect():
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='datamart_test',
            user='postgres',
            password='123')

        print('Conectado com o banco de dados')
        return conn
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)

def createTableToEtl(numberColumns):
    conn = connect()
