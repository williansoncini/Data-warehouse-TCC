from django.views import View
from django.shortcuts import redirect, render
from django.contrib import messages

class SelectFormInputView(View):
    
    def get(self, request):
        return render(request,'application/input/files/selectFormInput.html')

    def post(self, request):
        choiceInput = request.POST.get('options-file')
        print(choiceInput)
      

        if choiceInput == 'csv':
            print('to aqui')
            request.session['choiceInput'] = 'csv'
            return redirect ('application:csv-input')
        elif choiceInput == 'dump':
            request.session['choiceInput'] = 'dump'
            return redirect ('application:dump-input')
        elif choiceInput == 'sql':
            request.session['choiceInput'] = 'sql'
            return redirect ('application:sql-input')
        else:
            messages.warning(request, 'Select input form!')
            return render(request,'application/input/files/selectFormInput.html')
        