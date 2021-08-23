from ..database.stagingArea import connect
import csv
from ast import literal_eval

def makeNewCsvFile():
    file = open('upload/testedocsv.csv','w',encoding='UTF8')

    # writer = csv.writer(file, delimiter=';')
    # writer.writerow([1,'1'])

    file.close()

def getColumnsFromCsvFile(filePathAfterUpload):
    try:
        file = open(filePathAfterUpload,'r')
        csvFile = csv.reader(file, delimiter=';')
        columns = list(csvFile)[0]

        listColumns = []
        for index, column in enumerate(columns):
            if checkIfIsString(str(column)):
                listColumns.append(str(column))
            else:
                listColumns.append('column_{}'.format(index+1))

        file.close()
        return listColumns
    except:
        print('Erro ao pegar lista de colunas')

def getTypeOfColumnsFromCsvFile(filePathAfterUpload):
    try:
        file= open(filePathAfterUpload,'r')
        csvFile = csv.reader(file, delimiter=';')
            
        firstRowData = list(csvFile)[1]
        # print('firstRowData: ', firstRowData)

        listTypeOfData = []
        for data in firstRowData:
            listTypeOfData.append(getTypeData(data))

        parseTypeDataToSqlTypeData(listTypeOfData)

        file.close()

        # print(listTypeOfData)
        return listTypeOfData
    except:
        print('Erro ao pegar lista de tipos das colunas')
       

def checkIfIsString(string):
    if string.isdigit():
            # print('Esse campo é um numero')
            return False
    else:
        if string[0].isdigit():
            # print('A primeira letra é um número')
            return False
        else:
            return True
        
def getTypeData(data):
    stringData = str(data)
    try:
        dataAfterTratament = literal_eval(stringData)
        return type(dataAfterTratament)
        # print('Dado tratado: {} seu tipo: {}'.format(dataBeforeTratament,type(dataBeforeTratament)))
    except:
        return type(stringData)
        # print('Dado não tratado: {} seu tipo: {}'.format(stringData, type(stringData)))

def parseTypeDataToSqlTypeData(typeDatas):
    sqlTypeData = []

    for type in typeDatas:
        print(type)
        if type == str:
            sqlTypeData.append('VARCHAR')
        elif type == int:
            sqlTypeData.append('INT')
        elif type == float:
            sqlTypeData.append('DECIMAL')
        else:
            sqlTypeData.append('VARCHAR')
    print(sqlTypeData)
    # return sqlTypeData

def importCsvFileInTable(filePathAfterUpload):
    conn = connect()
    cur = conn.cursor()
    file = open(filePathAfterUpload, 'r')
    cur.copy_from(file,'teste_csv',sep=';')
    cur.close()

    conn.commit()
    print('conexão sendo fechada!')
    conn.close()
