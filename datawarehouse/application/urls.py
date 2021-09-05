from django.conf.urls import url
from application.views.dataInput import dataLoad, stagingArea
# from application.views.dataInput.stagingArea import StagingAreaView
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
    path('input/stagingArea/expression/<int:table_id>/<int:column_id>/', stagingArea.updateColumnStagingArea, name='updateStagingArea'),
    path('input/stagingArea/delete/<int:table_id>/<int:column_id>/', stagingArea.deleteColumnStagingArea, name='deleteStagingArea'),
    path('input/stagingArea/create/<int:table_id>/', stagingArea.createColumnStagingArea, name='createColumnStagingArea'),
    path('input/stagingArea/statement', stagingArea.statementView, name='stagingArea-statement')
    # path('input/stagingArea/expression/<int:table_id>/<int:column_id>/', StagingAreaView.put, name='updateStagingArea')
]