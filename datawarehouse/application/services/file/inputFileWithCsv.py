from ..database.connectStagingArea import connect
from django.core.files.storage import FileSystemStorage
import os

# module_dir = os.path.dirname(__file__)  # get current directory


def importCSVfile(nameFile):
    conn = connect()
    # file_path = os.path.join(module_dir, '..TESTE.CSV')
    # open(str(nameFile),'rb')
    # print('nameFile:',nameFile)
    # print('CAMINHO DO ARQUIVO:', file_path)
    # fs = FileSystemStorage()
    # file = fs.open(nameFile,'rb')
    cur = conn.cursor()
    file = open(nameFile, 'r')
    cur.copy_from(file,'teste_csv',sep=';')
    cur.close()

    conn.commit()
    print('conexão sendo fechada!')
    conn.close()
