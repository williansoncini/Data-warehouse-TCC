import psycopg2
from dotenv import load_dotenv
from os import getenv

def connectExternalDatamart(database, host, user, password, port):
    try:
        load_dotenv()
        conn = psycopg2.connect(
            database= database,
            host=host,
            user=user,
            password=password,
            port=port
        )
        return conn
    except:
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
    