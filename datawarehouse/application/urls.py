from application.views.datamart.tables.tableListView import TableListView
from application.views.datamart.tables.tableDeleteView import TableDeleteView
from application.views.datamart.datamart import DatamartView
from application.models import Datamart, TableDataMart
from django.conf.urls import url
from application.views.datamart.datamartDelete import DatamartDelete
from .views.dataInput import dataLoad, stagingArea
from .views.datamart.datamart import DatamartView
from .views.datamart.datamartUpdate import DatamartUpdate
from .views.datamart.datamartCreate import DatamartCreate
from .views.dataInput.datamart.selectDatamart import SelectDatamart
from .views.dataInput.datamart.selectTableDatamart import SelectTableDatamart
from .views.dataInput.files.selectFormInputView import SelectFormInputView
# from .views.datamart import Datamart
from .views.dataInput import csv,dump, query
from .views.home import home
from django.urls import path

app_name = 'application'

urlpatterns = [
    path('',home.getHome, name='home'),
    path('input/datamart',SelectDatamart.as_view(), name='select-datamart'),
    path('input/datamart/table',SelectTableDatamart.as_view(), name='select-table-datamart'),
    path('input/files/', SelectFormInputView.as_view(), name='files-input'),
    path('input/csv/', csv.inputCsvFile, name='csv-input'),
    path('input/dump/', dump.inputDumpFile, name='dump-input'),
    path('input/query/', query.inputFromQuerySQL, name='sql-input'),
    path('input/preImportFile/', dataLoad.showDataFromFile, name='data_load'),
    path('input/stagingArea', stagingArea.StagingAreaDetail, name='stagingArea'),
    path('input/stagingArea/deleteTable/<int:table_id>/', stagingArea.deleteTableStagingArea, name='deleteTableStagingArea'),
    path('input/stagingArea/updateColumn/<int:table_id>/<int:column_id>/', stagingArea.updateColumnStagingArea, name='updateStagingArea'),
    path('input/stagingArea/deleteColumn/<int:table_id>/<int:column_id>/', stagingArea.deleteColumnStagingArea, name='deleteStagingArea'),
    path('input/stagingArea/createColumn/<int:table_id>/', stagingArea.createColumnStagingArea, name='createColumnStagingArea'),
    path('input/stagingArea/statement', stagingArea.statementView, name='stagingArea-statement'),
    path('datamart/',DatamartView.as_view(), name='datamart-list'),
    path('datamart/create/',DatamartCreate.as_view(), name='datamart-create'),
    path('datamart/update/<int:datamart_id>/',DatamartUpdate.as_view(), name='datamart-detail'),
    path('datamart/delete/<int:datamart_id>',DatamartDelete.as_view(), name='datamart-delete'),
    path('datamart/tables',TableListView.as_view(), name='datamart-tables'),
    path('datamart/tables/delete/<int:table_id>',TableDeleteView.as_view(), name='datamart-tables-delete'),
    # path('datamart/',datamart.show, name='datamart-list')
]