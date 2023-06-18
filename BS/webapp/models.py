# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey has `on_delete` set to the desired behavior.
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Arr(models.Model):
    arrx = models.FloatField()
    arry = models.FloatField()
    arrz = models.FloatField()
    time = models.CharField(max_length=50)
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'arr'


class Datatable(models.Model):
    dip = models.IntegerField()
    temp = models.IntegerField()
    humi = models.IntegerField()
    mq = models.SmallIntegerField()
    qual = models.IntegerField()
    time = models.CharField(max_length=50)
    id = models.AutoField(db_column='ID', primary_key=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'datatable'


class Dht11(models.Model):
    temp = models.CharField(max_length=10)
    humi = models.CharField(max_length=10)
    time = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'dht11'


class User1(models.Model):
    name = models.CharField(unique=True, max_length=10)
    age = models.IntegerField()

    class Meta:
        managed = False
        db_table = 'user1'



class UserInfo(models.Model):
    username = models.CharField(max_length = 32,blank='True')
    password = models.CharField(max_length = 64)