from django.urls import path
from . import views

app_name = 'application'

urlpatterns = [
    path('',views.datamart_list, name='datamart_list'),
    path('/teste/file', views.fileinput, name='file_input'),
    path('/teste/query', views.queryInput, name='query_input'),
    # path('/file', views.fileinput, name='file_input'),
]