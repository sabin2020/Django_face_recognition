from django.db import models
from datetime import datetime
# Create your models here.
class Employee(models.Model):
    name = models.CharField(max_length=200)
    phone = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    address = models.CharField(max_length=200)
    photo = models.ImageField(upload_to='%y/%m/%d')
    work_hour = models.IntegerField()
    in_time = models.TimeField(blank=True)
    out_time = models.TimeField(blank=True)
    time_outside_office = models.DurationField(blank=True)
    how_many_times = models.IntegerField(blank=True)
    in_out = models.BooleanField(default=False,blank=True)
    def __str__(self):
        return self.name
