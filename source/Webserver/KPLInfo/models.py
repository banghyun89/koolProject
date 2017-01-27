from django.db import models

# Create your models here.


class Obd(models.Model):
    id = models.IntegerField(primary_key=True)
    time = models.DateTimeField()
    vss = models.DecimalField(decimal_places=2,max_digits=10)
    maf = models.DecimalField(decimal_places=2,max_digits=10)
    kpl = models.DecimalField(decimal_places=2,max_digits=10)
