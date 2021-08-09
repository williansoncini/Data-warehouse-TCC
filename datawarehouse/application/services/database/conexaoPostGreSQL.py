import psycopg2
# from file.fileService import getAbsolutePath

def connect():
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='datamart_test',
            user='postgres',
            password='123')

        cur = conn.cursor()
        file = open(r'C:\Users\Computador\OneDrive\Faculdade\OITAVO SEMESTRE\TCC\Aplicacao\Data-warehouse-TCC\datawarehouse\application\upload\TESTE.CSV', 'r')
        cur.copy_from(file,'teste_csv',sep=';')
        # cur.execute("copy TESTE_CSV(ID,NAME) from 'C:\TESTE\TESTE.CSV' delimiter ';' csv header;")
        # print(getAbsolutePath('TESTE.CSV'))
        # cur.execute("copy TESTE_CSV(ID,NAME) from '{}' delimiter ';' csv header;".format(getAbsolutePath('TESTE.CSV')))
        
        # data_base = cur.fetchall()
        # for db in data_base:
        #     print(db)
        conn.commit()
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Conexão fechada')

connect()