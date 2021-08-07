from django.db import models

# Create your models here.
class Datamart(models.Model):
    STATUS_CHOICES = (
        ('active','Active',),
        ('incative','Inactive'),
    )

    name = models.CharField(max_length=250)
    updated = models.DateTimeField(auto_now=True)
    status = models.CharField(max_length=20,choices=STATUS_CHOICES,default='Active')

    class Meta:
        ordering = ('-updated',)

    def __str__(self):
        return self.name