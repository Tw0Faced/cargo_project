# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class Cargo(models.Model):
    g_id = models.AutoField(primary_key=True)
    g_name = models.CharField(max_length=50)
    g_weight = models.DecimalField(max_digits=10, decimal_places=2)
    g_volume = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    g_type = models.CharField(max_length=20, blank=True, null=True)
    c = models.ForeignKey('Clients', models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'cargo'


class Clients(models.Model):
    c_id = models.AutoField(primary_key=True)
    c_type = models.CharField(max_length=2)
    c_name = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'clients'


class Dispatchers(models.Model):
    d_id = models.AutoField(primary_key=True)
    d_name = models.CharField(max_length=50)
    d_email = models.CharField(unique=True, max_length=50)
    d_pass = models.CharField(max_length=99)

    class Meta:
        managed = False
        db_table = 'dispatchers'


class DriverLicense(models.Model):
    pk = models.CompositePrimaryKey('dr_id', 'l_id')
    dr = models.ForeignKey('Drivers', models.DO_NOTHING)
    l = models.ForeignKey('Licenses', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'driver_license'


class Drivers(models.Model):
    dr_id = models.AutoField(primary_key=True)
    dr_name = models.CharField(max_length=50)
    dr_tel = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'drivers'


class Individuals(models.Model):
    c = models.OneToOneField(Clients, models.DO_NOTHING, primary_key=True)
    p_passp = models.CharField(max_length=50)
    p_date = models.DateField(blank=True, null=True)
    p_tel = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'individuals'


class LegalEntities(models.Model):
    c = models.OneToOneField(Clients, models.DO_NOTHING, primary_key=True)
    y_inn = models.BigIntegerField(unique=True)
    y_tel = models.CharField(max_length=30, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'legal_entities'


class Licenses(models.Model):
    l_id = models.AutoField(primary_key=True)
    l_name = models.CharField(max_length=2)

    class Meta:
        managed = False
        db_table = 'licenses'


class Routes(models.Model):
    r_id = models.AutoField(primary_key=True)
    r_from = models.CharField(max_length=50)
    r_to = models.CharField(max_length=50)
    r_dist = models.IntegerField(blank=True, null=True)
    r_time = models.IntegerField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'routes'


class Shipments(models.Model):
    tr_id = models.AutoField(primary_key=True)
    cargo = models.ForeignKey(Cargo, models.DO_NOTHING, blank=True, null=True)
    transport = models.ForeignKey('Transports', models.DO_NOTHING, blank=True, null=True)
    route = models.ForeignKey(Routes, models.DO_NOTHING, blank=True, null=True)
    client = models.ForeignKey(Dispatchers, models.DO_NOTHING, blank=True, null=True)
    tr_date_start = models.DateField()
    tr_date_end = models.DateField(blank=True, null=True)
    tr_status = models.CharField(max_length=20, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'shipments'


class Transports(models.Model):
    t_id = models.AutoField(primary_key=True)
    t_mark = models.CharField(max_length=30)
    t_model = models.CharField(max_length=30)
    t_number = models.CharField(unique=True, max_length=15)
    t_cap = models.IntegerField()
    dr = models.ForeignKey(Drivers, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'transports'
