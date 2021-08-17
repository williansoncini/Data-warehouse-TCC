from django.contrib import admin
from .models import Datamart, TableDataMart, ColumnDataMart, TypeData
# Register your models here.
admin.site.register(Datamart)
admin.site.register(TableDataMart)
admin.site.register(ColumnDataMart)
admin.site.register(TypeData)
