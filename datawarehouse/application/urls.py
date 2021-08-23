from django.urls import path
# from . import views
from .views.dataInput import csv,dump, query
from .views.home import home
from .views.sideMenu import sideMenu

app_name = 'application'

urlpatterns = [
    path('',home.getHome, name='home'),
    path('input/', sideMenu.getMenuInput, name='menu_input'),
    path('input/csv/', csv.inputCsvFile, name='csv_input'),
    path('input/query/', query.inputFromQuerySQL, name='query_input'),
    path('input/dump/', dump.inputDumpFile, name='dump_input'),
]