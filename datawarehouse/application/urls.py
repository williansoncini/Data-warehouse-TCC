from django.urls import path
from . import views

app_name = 'application'

urlpatterns = [
    # path('',views.datamart_list, name='datamart_list'),
    path('',views.getHome, name='home'),
    path('/input/', views.getMenuInput, name='menu_input'),
    # path('/input/', views.listOfFormsImportations, name='list_forms_importations'),
    path('/input/csv', views.fileinput, name='csv_input'),
    path('/input/query', views.queryInput, name='query_input'),
    path('/input/dump', views.inputDumpFile, name='dump_input'),
]