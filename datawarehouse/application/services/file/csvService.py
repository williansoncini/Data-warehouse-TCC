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
            if checkIfIsString(column):
                listColumns.append(column)
            else:
                listColumns.append('column_{}'.format(index+1))

        file.close()
        return listColumns
    except Exception as e:
        print('Erro ao pegar lista de colunas')
        print(e)

def getTypeOfColumnsFromCsvFile(filePathAfterUpload):
    try:
        file= open(filePathAfterUpload,'r')
        csvFile = csv.reader(file, delimiter=';')
            
        firstRowData = list(csvFile)[1]
        # print('firstRowData: ', firstRowData)

        listTypeOfData = []
        for data in firstRowData:
            listTypeOfData.append(getTypeData(data))

        listTypeOfData = parseTypeDataToSqlTypeData(listTypeOfData)

        file.close()

        # print(listTypeOfData)
        return listTypeOfData
    except:
        print('Erro ao pegar lista de tipos das colunas')

def getTypeData(data):
    # print(data)
    try:
        dataAfterTratament = literal_eval(data)
        return type(dataAfterTratament)
        # print('Dado tratado: {} seu tipo: {}'.format(dataBeforeTratament,type(dataBeforeTratament)))
    except:
        return type(data)
        # print('Dado não tratado: {} seu tipo: {}'.format(stringData, type(stringData)))    

def checkIfIsString(data):
    data = getTypeData(data)
    if data == str:
        # print('Esse campo é um numero')
        return True
    else:
        # print('A primeira letra é um número')
        return False

def parseTypeDataToSqlTypeData(typeDatas):
    sqlTypeData = []

    for type in typeDatas:
        # print(type)
        if type == str:
            sqlTypeData.append('VARCHAR')
        elif type == int:
            sqlTypeData.append('INT')
        elif type == float:
            sqlTypeData.append('DECIMAL')
        else:
            sqlTypeData.append('VARCHAR')
    # print('teste')
    # print(sqlTypeData)
    return sqlTypeData

def makeDicWithColumnType(columns, types):
    dictionarie = {}
    for index, column in enumerate(columns):
        # print('dicionario coluna: {}'.format(column))
        # print('dicionario tipo: {}'.format(types[index]))
        dictionarie[column] = types[index]

    return dictionarie

# def handleUploadedFile(file):
#     with open(,'r') as file:
def getFirstTwentyLinesFromFile(filePath):
    data = []
    with open(filePath,'r') as file:
        csvFile = csv.reader(file, delimiter=';')
        for index, line in enumerate(csvFile):
            if index < 20:
                data.append(line)
            else:
                break

    # parseDataToList(data)
    # print(data[0])
    return data

def makeFakeColumnsFromCsvFile(filePathAfterUpload):
    try:
        with open(filePathAfterUpload,'r') as file:
            csvFile = csv.reader(file, delimiter=';')
            columns = list(csvFile)[0]

            listColumns = []
            for index, column in enumerate(columns):
                listColumns.append('column_{}'.format(index+1))

        return listColumns
    except Exception as e:
        print('Erro ao pegar lista de colunas')
        print(e)
