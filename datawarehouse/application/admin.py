from django.contrib import admin
from .models import ColumnStagingArea, Datamart, ExtractConnection, TableDataMart, ColumnDataMart, TableStagingArea
# Register your models here.
admin.site.register(ExtractConnection)

admin.site.register(TableStagingArea)
admin.site.register(ColumnStagingArea)

admin.site.register(Datamart)
admin.site.register(TableDataMart)
admin.site.register(ColumnDataMart)
