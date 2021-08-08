import os

def handle_uploaded_file(file):
    with open('application/upload/'+file.name,'wb+') as destination:
        for chunk in file.chunks():
            destination.write(chunk)    

def getAbsolutePath(nameFile):
    return os.path.abspath('application/upload/'+nameFile)
    