import abc
from django.db import models
from django.db.models.deletion import CASCADE

# Create your models here.
class Datamart(models.Model):
    STATUS_CHOICES = (
        ('active','Active',),
        ('incative','Inactive'),
    )

    name = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Active')

    class Meta:
        ordering = ('-name',)

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
        ordering = ('-name',)

    def __str__(self):
        return self.name

class TypeData(models.Model):
    TYPES_DATABASE = (
        ('int', 'INT'),
        ('varchar(250)', 'VARCHAR(250)'),
        ('varchar(#)', 'VARCHAR(#)'),
        ('char(1)','CHAR(1)'),
        ('double(14,4)','DOUBLE(14,4)'),
        ('double(#,#)','DOUBLE(#,#)'),
    )

    TYPES_SIMPLE = (
        ('text', 'TEXT'),
        ('text(#)', 'TEXT(#)'),
        ('number','NUMBER'),
        ('number(#,#)','NUMBER(#,#)'),
    )

    # teste = models.CharField(max_length=250)
    typeSimple = models.CharField(max_length=50, choices=TYPES_SIMPLE)
    typeDataBase = models.CharField(max_length=50, choices=TYPES_DATABASE)

    class Meta:
        ordering = ('-typeSimple',)
        # ordering = ('-teste',)

    def __str__(self):
        return self.typeSimple
        # return self.teste

class ColumnDataMart(models.Model):
    table = models.ForeignKey(TableDataMart, on_delete=models.CASCADE, related_name='column_datamart')
    typeSimple = models.ForeignKey(TypeData, on_delete=models.CASCADE, related_name='column_typeSimple')
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ('-name',)

    def __str__(self):
        return self.name

