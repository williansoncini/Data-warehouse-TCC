import csv

def makeCSVFile():
    file = open('upload/testedocsv.csv','w',encoding='UTF8')

    # writer = csv.writer(file, delimiter=';')
    # writer.writerow([1,'1'])

    file.close()
