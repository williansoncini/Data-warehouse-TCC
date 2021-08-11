from django.urls import path
from . import views

app_name = 'application'

urlpatterns = [
    path('',views.datamart_list, name='datamart_list'),
    path('/input/', views.listOfFormsImportations, name='list_forms_importations'),
    # path('/input/file', views.fileinput, name='file_input'),
    # path('/input/query', views.queryInput, name='query_input'),
]