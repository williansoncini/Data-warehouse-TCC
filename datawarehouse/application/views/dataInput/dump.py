from django.shortcuts import render
from django.core.files.storage import FileSystemStorage
from application.services.database.stagingArea import connect

def inputDumpFile(request):
    retorno = {}
    if request.method == 'POST':

        file = request.FILES['dumpFile']
        fs = FileSystemStorage()
        name = fs.save(file.name, file)
        url = fs.url(name)

        # importCSVfile(str(url[1:]))
        # Aqui tem que fazer um tratamento de dados para não aceitar '`'
        with open (str(url[1:]),'r',encoding='UTF8') as dumpFile:
            conn = connect()
            cur = conn.cursor()
            cur.execute("""{}""".format(dumpFile.read().replace('`','')))
            cur.close()
            conn.commit()
            conn.close()

        retorno['mensagem'] = 'Arquivo DUMP carregado com sucesso!'

    return render(request, 'application/input/inputDump.html',retorno)