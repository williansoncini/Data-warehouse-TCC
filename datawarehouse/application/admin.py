from django.contrib import admin
from .models import ColumnStagingArea, Datamart, TableDataMart, ColumnDataMart, TableStagingArea
# Register your models here.
admin.site.register(Datamart)
# admin.site.register(DatamartConnection)
admin.site.register(TableDataMart)
admin.site.register(ColumnDataMart)

admin.site.register(TableStagingArea)
admin.site.register(ColumnStagingArea)
