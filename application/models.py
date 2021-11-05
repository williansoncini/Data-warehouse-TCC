from typing import Callable
from django.db import models
from django.db.models.deletion import CASCADE
from django.db.models.fields import BooleanField, CharField, DateTimeField, IntegerField, TextField
from django.db.models.fields.related import ForeignKey

class Datamart(models.Model):
    STATUS_CHOICES = (
        ('active','Active',),
        ('incative','Inactive'),
    )
    name = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Active')
    database = CharField(max_length=50)
    user = CharField(max_length=50)
    password = CharField(max_length=50)
    host = CharField(max_length=20)
    port = IntegerField()
    localdatabase = BooleanField(default='0')

    class Meta:
        ordering = ('-updated',)

    def __str__(self):
        return self.name

class TableDataMart(models.Model):
    STATUS_CHOICES = (
        ('active','Active'),
        ('inactive', 'Inactive'),
    )
    datamart = models.ForeignKey(Datamart, related_name='table_datamart', on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Active')
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-updated',)

    def __str__(self):
        return self.name

class ColumnDataMart(models.Model):
    table = models.ForeignKey(TableDataMart, on_delete=models.CASCADE, related_name='column_datamart')
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name

class CsvFile(models.Model):
    name = models.CharField(max_length=250)
    size = models.FloatField()
    uploadDate = models.DateTimeField(auto_now_add=True)
    withHeader = models.BooleanField()

    def __str__(self):
        return self.name

class TemporaryFile(models.Model):
    name = models.CharField(max_length=250)
    filePath = models.TextField()
    
    class Meta:
        ordering = ('name',)

    def __str__(self):
        return self.name

class TableStagingArea(models.Model):
    tableName = CharField(max_length=250)
    statementCreateTable = TextField(null=True)
    statementSelect = TextField(null=True)
    
    def __str__(self):
        return self.tableName

class ColumnStagingArea(models.Model):
    table = ForeignKey(TableStagingArea, on_delete=models.CASCADE,related_name='stagingarea_table_column')
    name = CharField(max_length=250)
    TYPES_COLUMN = (
        ('INT','INT'),
        ('VARCHAR','VARCHAR'),
        ('FLOAT','FLOAT'),
    )
    typeColumn = CharField(max_length=30,choices=TYPES_COLUMN)

    def __str__(self):
        return self.name

class importationDatamart(models.Model):
    datamart = ForeignKey(Datamart, on_delete=CASCADE,related_name='importation_datamart')
    tableDatamart = ForeignKey(TableDataMart, on_delete=CASCADE, related_name='importation_tableDatamart')
    type = CharField(max_length=10)
    created = DateTimeField(auto_now_add=True)

class ExtractConnection(models.Model):
    name = models.CharField(max_length=250, unique=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    database = CharField(max_length=50)
    user = CharField(max_length=50)
    password = CharField(max_length=50)
    host = CharField(max_length=20)
    port = IntegerField()
    localdatabase = BooleanField(default='0')

    def __str__(self):
        return self.name

class TableDatawarehouse(models.Model):
    name = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    # status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Active')
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-updated',)

    def __str__(self):
        return self.name

class ColumnsDatawarehouse(models.Model):
    table = models.ForeignKey(TableDatawarehouse, on_delete=models.CASCADE, related_name='column_datawarehouse')
    name = models.CharField(max_length=50)
    type = models.CharField(max_length=50)

    class Meta:
        ordering = ('id',)

    def __str__(self):
        return self.name