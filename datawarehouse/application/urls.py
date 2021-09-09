from django.conf.urls import url
from .views.dataInput import dataLoad, stagingArea
from .views.datamart import datamart
from .views.dataInput import csv,dump, query
from .views.home import home
from django.urls import path

app_name = 'application'

urlpatterns = [
    path('',home.getHome, name='home'),
    path('input/csv/', csv.inputCsvFile, name='csv_input'),
    path('input/query/', query.inputFromQuerySQL, name='query_input'),
    path('input/dump/', dump.inputDumpFile, name='dump_input'),
    path('input/preImportFile/', dataLoad.showDataFromFile, name='data_load'),
    path('input/stagingArea', stagingArea.showTableDetail, name='stagingArea'),
    path('input/stagingArea/deleteTable/<int:table_id>/', stagingArea.deleteTableStagingArea, name='deleteTableStagingArea'),
    path('input/stagingArea/updateColumn/<int:table_id>/<int:column_id>/', stagingArea.updateColumnStagingArea, name='updateStagingArea'),
    path('input/stagingArea/deleteColumn/<int:table_id>/<int:column_id>/', stagingArea.deleteColumnStagingArea, name='deleteStagingArea'),
    path('input/stagingArea/createColumn/<int:table_id>/', stagingArea.createColumnStagingArea, name='createColumnStagingArea'),
    path('input/stagingArea/statement', stagingArea.statementView, name='stagingArea-statement'),
    path('datamart/',datamart.show, name='datamart-list')
]