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

def createTableForEtl(nameTable, columnsAndTypes):
    # conn = connect()
    statement = 'CREATE TABLE IF NOT EXISTS {} ( \n'.format(nameTable)
    for key, value in columnsAndTypes.items():
        statement += '{} {}; \n'.format(key, value)
    statement += ');'

    print(statement)


def importCsvFileInTable(filePath, nameTable):
    conn = connect()
    cur = conn.cursor()
    file = open(filePath, 'r')

    cur.copy_from(file,'teste_csv',sep=';')
    cur.close()

    conn.commit()
    print('conexão sendo fechada!')
    conn.close()
