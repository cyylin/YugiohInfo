# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models

class Cardtyperef(models.Model):
    cardtype = models.IntegerField(db_column='CardType', primary_key=True)  # Field name made lowercase.
    cardtypedesc = models.CharField(db_column='CardTypeDesc', max_length=10)  # Field name made lowercase.

    class Meta:
        db_table = 'CardTypeRef'


class Dailybind(models.Model):
    ProdId = models.CharField(db_column='ProdId', max_length=20)  # Field name made lowercase.
    ProdName = models.CharField(db_column='ProdName', max_length=10000, blank=True, null=True)  # Field name made lowercase.
    CardNo = models.CharField(db_column='CardNo', max_length=20)  # Field name made lowercase.
    CardType = models.IntegerField(db_column='CardType')  # Field name made lowercase.
    Spec = models.CharField(db_column='Spec', max_length=50, blank=True, null=True)  # Field name made lowercase.
    SpecSub = models.CharField(db_column='SpecSub', max_length=50, blank=True, null=True)  # Field name made lowercase.
    Price = models.IntegerField(db_column='Price')  # Field name made lowercase.
    Currency = models.CharField(db_column='Currency', max_length=10)  # Field name made lowercase.
    Qty = models.IntegerField(db_column='Qty')  # Field name made lowercase.
    LogDate = models.DateField(db_column='LogDate')  # Field name made lowercase.
    id = models.BigAutoField(primary_key=True)

    class Meta:
        db_table = 'DailyBind'


class Registercard(models.Model):
    cardno = models.CharField(db_column='CardNo', primary_key=True, max_length=20)  # Field name made lowercase.
    cardid = models.CharField(db_column='CardId', max_length=20, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        db_table = 'RegisterCard'
