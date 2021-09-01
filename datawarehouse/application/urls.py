from django.conf.urls import url
from application.views.dataInput import dataLoad, stagingArea
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
    path('input/preImportFile/', dataLoad.showDataFromFile, name='data_load'),
    path('input/stagingArea', stagingArea.showTableDetail, name='stagingArea'),
    path(r'^modal/', stagingArea.modal, name='modal'),
]