from django.views import View
from django.shortcuts import redirect, render

class SelectFormInputView(View):
    
    def get(self, request):
        return render(request,'application/input/files/selectFormInput.html')

    def post(self, request):
        choiceInput = request.POST.get('options-files')

        if choiceInput == 'csv':
            request.session['choiceInput'] = 'csv'
            return redirect ('application:csv-input')
        elif choiceInput == 'dump':
            request.session['choiceInput'] = 'dump'
            return redirect ('application:dump-input')
        elif choiceInput == 'sql':
            request.session['choiceInput'] = 'sql'
            return redirect ('application:sql-input')
        else:
            return render(request,'application/input/files/selectFormInput.html')

        