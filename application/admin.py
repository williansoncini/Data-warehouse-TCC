from django.contrib import admin
from .models import ColumnStagingArea, ColumnsDatawarehouse, CubeColumnsDatawarehouse, CubeDatawarehouse, Datamart, ExtractConnection, TableDataMart, ColumnDataMart, TableDatawarehouse, TableStagingArea
# Register your models here.
admin.site.register(ExtractConnection)

admin.site.register(TableStagingArea)
admin.site.register(ColumnStagingArea)

admin.site.register(Datamart)
admin.site.register(TableDataMart)
admin.site.register(ColumnDataMart)

admin.site.register(TableDatawarehouse)
admin.site.register(ColumnsDatawarehouse)

admin.site.register(CubeDatawarehouse)
admin.site.register(CubeColumnsDatawarehouse)