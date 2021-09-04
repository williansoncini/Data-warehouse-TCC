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

    dropTableStatement = 'DROP TABLE IF EXISTS {};'.format(nameTable)
    createTableStatement = 'CREATE TABLE IF NOT EXISTS {} ('.format(nameTable)

    
    for index, (key, value) in enumerate(columnsAndTypes.items()):
        if index +1 == len(columnsAndTypes):
            createTableStatement += '{} {}'.format(str(key).replace(' ','_'), value)
        else:
            createTableStatement += '{} {},'.format(str(key).replace(' ','_'), value)
    createTableStatement += ');'
    # print(statement)

    conn = connect()
    cur = conn.cursor()
    cur.execute(dropTableStatement)
    conn.commit()
    cur.execute(createTableStatement)
    conn.commit()
    cur.close()
    conn.close()

def importCsvFileInTableWithHeader(filePath, nameTable):
    conn = connect()
    cur = conn.cursor()
    file = open(filePath, 'r')
    cur.copy_expert("COPY {} FROM STDOUT WITH CSV HEADER DELIMITER ';'".format(nameTable),file)
    # cur.copy_from(file,nameTable,sep=';')
    cur.close()

    conn.commit()
    print('conexão sendo fechada!')
    conn.close()  

def importCsvFileInTableWithOutHeader(filePath, nameTable):
    conn = connect()
    cur = conn.cursor()
    file = open(filePath, 'r')
    cur.copy_from(file,nameTable,sep=';')
    cur.close()

    conn.commit()
    print('conexão sendo fechada!')
    conn.close()  

def makeSelectStatement(nameTable, Columns):
    statement = 'SELECT\n' 
    lenColumns = len(Columns)
    for index, column in enumerate(Columns):
        if index+1 == lenColumns:
                statement += '  {}\n'.format(column.name)
        else:
                statement += '  {},\n'.format(column.name)
    statement += 'FROM \n   {}'.format(nameTable)
    return statement

def makeStatementCreateTable(tableName, Columns):
    statement = 'DROP TABLE IF EXISTS {};\n'.format(tableName)
    statement += 'CREATE TABLE IF NOT EXISTS {} ('.format(tableName)

    lenColumns = len(Columns)
    for index, column in enumerate(Columns):
        if index +1 == lenColumns:
            statement += '{} {}'.format(column.name, column.typeColumn)
        else:
            statement += '{} {},'.format(column.name, column.typeColumn)
    statement += ');'

    return statement