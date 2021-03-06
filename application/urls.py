from application.views.dataInput.ExtractConnetions.extractConnectionCreateView import ExtractConnectionCreateView
from application.views.dataInput.ExtractConnetions.extractConnectionDeleteView import ExtractConnectionDeleteView
from application.views.dataInput.ExtractConnetions.extractConnectionListView import ExtractConnectionsListView
from application.views.dataInput.ExtractConnetions.extractConnectionUpdateView import ExtractConnectionUpdateView
from application.views.dataInput.dataLoad import DataloadView
from application.views.dataInput.dump import DumpFile
from application.views.dataInput.query import QueryInput
from application.views.datamart.tables.columns.createColumnView import CreateColumnDatamartView
from application.views.datamart.tables.columns.deleteColumnDatamartView import DeleteColumnDatamartView
from application.views.datamart.tables.columns.updateColumnDatamartView import UpdateColumnDatamartView
from application.views.datamart.tables.pre_TableCreateView import PreTableDatamartCreateView
from application.views.datamart.tables.tableCreateView import TableDatamartCreateView
from application.views.datamart.tables.tableListView import TableDatamartListView
from application.views.datamart.tables.tableDeleteView import TableDatamartDeleteView
from application.views.datamart.datamart import DatamartView
from application.views.datamart.datamartDelete import DatamartDelete
from application.views.datamart.tables.tableUpdateView import TableDatamartUpdateView
from application.views.datawarehouse.cubes.create.selectColumns import SelectColumns
from application.views.datawarehouse.cubes.create.selectTables import SelectTablesForCube
from application.views.datawarehouse.cubes.deleteCube import DeleteCube
from application.views.datawarehouse.cubes.listCubes import ListCubes
from application.views.datawarehouse.input.dataLoad import DatawarehouseDataLoad
from application.views.datawarehouse.input.queryDatamart import QueryDatamartDatawarehouse
from application.views.datawarehouse.tables.deleteTableDatawarehouse import DatawarehouseDeleteTable
from application.views.datawarehouse.tables.listTableDatawarehouse import ListTableDatawarehouse
from application.views.datawarehouse.input.selectDatamart import SelectDatamartToDatawarehouse
from .views.dataInput import stagingArea
from .views.datamart.datamart import DatamartView
from .views.datamart.datamartUpdate import DatamartUpdate
from .views.datamart.datamartCreate import DatamartCreate
from .views.dataInput.datamart.selectDatamart import SelectDatamart
from .views.dataInput.datamart.selectTableDatamart import SelectTableDatamart
from .views.dataInput.files.selectFormInputView import SelectFormInputView
from .views.dataInput import csv
from .views.home import home
from django.urls import path

app_name = 'application'

urlpatterns = [
    path('',home.getHome, name='home'),

    path('input/datamart',SelectDatamart.as_view(), name='select-datamart'),
    path('input/datamart/table',SelectTableDatamart.as_view(), name='select-table-datamart'),
    path('input/files/', SelectFormInputView.as_view(), name='files-input'),
    path('input/csv/', csv.inputCsvFile, name='csv-input'),
    path('input/dump/', DumpFile.as_view(), name='dump-input'),
    path('input/query/', QueryInput.as_view(), name='sql-input'),
    path('input/preImportFile/', DataloadView.as_view(), name='data_load'),

    path('input/Extractconnections/', ExtractConnectionsListView.as_view(), name='extract-connections'),
    path('input/Extractconnections/create', ExtractConnectionCreateView.as_view(), name='extract-connections-create'),
    path('input/Extractconnections/update/<int:extractConnection_id>/', ExtractConnectionUpdateView.as_view(), name='extract-connections-update'),
    path('input/Extractconnections/delete/<int:extractConnection_id>/', ExtractConnectionDeleteView.as_view(), name='extract-connections-delete'),

    path('input/stagingArea', stagingArea.StagingAreaDetail, name='stagingArea'),
    path('input/stagingArea/deleteTable/<int:table_id>/', stagingArea.deleteTableStagingArea, name='deleteTableStagingArea'),
    path('input/stagingArea/updateColumn/<int:table_id>/<int:column_id>/', stagingArea.updateColumnStagingArea, name='updateStagingArea'),
    path('input/stagingArea/deleteColumn/<int:table_id>/<int:column_id>/', stagingArea.deleteColumnStagingArea, name='deleteStagingArea'),
    path('input/stagingArea/createColumn/<int:table_id>/', stagingArea.createColumnStagingArea, name='createColumnStagingArea'),
    path('input/stagingArea/statement', stagingArea.statementView, name='stagingArea-statement'),

    path('datamart/',DatamartView.as_view(), name='datamart-list'),
    path('datamart/create/',DatamartCreate.as_view(), name='datamart-create'),
    path('datamart/update/<int:datamart_id>/',DatamartUpdate.as_view(), name='datamart-detail'),
    path('datamart/delete/<int:datamart_id>/',DatamartDelete.as_view(), name='datamart-delete'),

    path('datamart/tables/',TableDatamartListView.as_view(), name='datamart-tables'),
    path('datamart/tables/pre-create/',PreTableDatamartCreateView.as_view(), name='datamart-tables-pre-create'),
    path('datamart/tables/create/<int:table_id>/',TableDatamartCreateView.as_view(), name='datamart-tables-create'),
    path('datamart/tables/update/<int:table_id>/',TableDatamartUpdateView.as_view(), name='datamart-tables-update'),
    path('datamart/tables/delete/<int:table_id>/',TableDatamartDeleteView.as_view(), name='datamart-tables-delete'),

    path('datamart/tables/columns/create/<int:table_id>/',CreateColumnDatamartView.as_view(), name='datamart-columns-create'),
    path('datamart/tables/columns/update/<int:table_id>/<int:column_id>/',UpdateColumnDatamartView.as_view(), name='datamart-columns-update'),
    path('datamart/tables/columns/delete/<int:table_id>/<int:column_id>/',DeleteColumnDatamartView.as_view(), name='datamart-columns-delete'),

    path('datawarehouse/import/datamart', SelectDatamartToDatawarehouse.as_view(), name='datawarehouse-import-select-datamart'),
    path('datawarehouse/import/datamart/query', QueryDatamartDatawarehouse.as_view(), name='datawarehouse-import-datamart-query'),
    path('datawarehouse/tables/dataload', DatawarehouseDataLoad.as_view(), name='datawarehouse-import-tables-data-load'),
    path('datawarehouse/tables/', ListTableDatawarehouse.as_view(), name='datawarehouse-tables'),
    path('datawarehouse/tables/delete/<int:table_id>/', DatawarehouseDeleteTable.as_view(), name='datawarehouse-tables-delete'),
    path('datawarehouse/cubes/', ListCubes.as_view(), name='datawarehouse-cubes'),
    path('datawarehouse/cubes/create/select-tables', SelectTablesForCube.as_view(), name='datawarehouse-cubes-select-tables'),
    path('datawarehouse/cubes/create/select-tables/columns', SelectColumns.as_view(), name='datawarehouse-cubes-select-tables-cubes'),
    path('datawarehouse/cubes/delete/<int:cube_id>/', DeleteCube.as_view(), name='datawarehouse-cubes-delete'),
    # path('datamart/tables/columns/update/<int:table_id>/<int:column_id>/',UpdateColumnDatamartView.as_view(), name='datamart-columns-update'),
    # path('datamart/tables/columns/delete/<int:table_id>/<int:column_id>/',DeleteColumnDatamartView.as_view(), name='datamart-columns-delete'),
]