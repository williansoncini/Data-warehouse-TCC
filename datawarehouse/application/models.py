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
    datamart = models.ForeignKey(Datamart, related_name='tabelas', on_delete=models.CASCADE)
    name = models.CharField(max_length=250)
    created = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Active')
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ('-name',)

    def __str__(self):
        return self.name

class TypeData(models.Model):

    type = models.CharField(max_length=50)

    class Meta:
        ordering = ('-type',)

    def __str__(self):
        return self.type

class ColumnDataMart(models.Model):
    table = models.ForeignKey(TableDataMart, on_delete=models.CASCADE, related_name='colunas')
    type = models.ForeignKey(TypeData, on_delete=models.CASCADE, related_name='tipo')
    name = models.CharField(max_length=50)

    class Meta:
        ordering = ('-name',)

    def __str__(self):
        return self.name

