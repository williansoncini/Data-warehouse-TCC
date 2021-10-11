from application.models import TemporaryFile
# from ...forms import inputFileForm
from os.path import splitext
from django.shortcuts import redirect, render
from django.core.files.storage import FileSystemStorage
from django.contrib import messages

class File(object):
    def __init__(self, nome, filePath):
        self.nome = nome
        self.filePath = filePath

    def getName(self):
        return self.nome

    def getFilePath(self):
        return self.filePath

def inputCsvFile(request):
    columns = []
    typeColumns = []
    if request.method == 'POST':
        try:
            try:
                file = request.FILES['file']
            except:
                messages.warning(request, 'Select file!')
                return render(request, 'application/input/inputCsv.html')
            nameFile = formatFileName(str(file))
            
            filePathAfterUpload = saveCsvFileAndReturnFilePath(request.FILES['file'])
            fileSize =  getSizeFile(filePathAfterUpload)
            (temporaryFile,__) = TemporaryFile.objects.get_or_create(name=nameFile, filePath=filePathAfterUpload, size=fileSize)
            request.session['tempFilePk'] = temporaryFile.id
            
            return redirect('application:data_load')
        except OSError as err:
            print(err)
            return render(request, 'application/input/inputCsv.html', getFailMessage())
    else:    
        return render(request, 'application/input/inputCsv.html')

def saveCsvFileAndReturnFilePath(file):
    fileSystem = FileSystemStorage()
    newName = fileSystem.save(file.name, file)
    return fileSystem.path(newName)

def getSucessMessage():
    sucessMessage = 'Arquivo carregado com sucesso!'
    return sucessMessage

def getFailMessage():
    failMessage = {'message': 'Falha ao carregar arquivo'}
    return failMessage

def formatFileName(name):
    nameWithOutExtension = splitext(name)[0]

    remove = [
        '.',
        ' ',
        '-'
    ]

    for char in remove:
        nameWithOutExtension = nameWithOutExtension.replace(char,'_')

    nameWithOutExtension = nameWithOutExtension.lower()
    return nameWithOutExtension

def getSizeFile(name):
    fileSystem = FileSystemStorage()
    return fileSystem.size(name)