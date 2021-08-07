# https://www.postgresqltutorial.com/postgresql-python/connect/

import psycopg2

def connect():
    try:
        conn = psycopg2.connect(
            host='localhost',
            database='base_teste',
            user='postgres',
            password='123')

        cur = conn.cursor()
        
        print('Versão do PostgreSQL')
        cur.execute('select DATNAME from PG_DATABASE')
        data_base = cur.fetchall()
        for db in data_base:
            print(db)
        
        cur.close()
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()
            print('Conexão fechada')

if __name__ == '__main__':
    connect()