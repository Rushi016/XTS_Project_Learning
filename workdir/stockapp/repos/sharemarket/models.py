# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from django.db import models


class AuthGroup(models.Model):
    name = models.CharField(unique=True, max_length=150)

    class Meta:
        managed = False
        db_table = 'auth_group'


class AuthGroupPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)
    permission = models.ForeignKey('AuthPermission', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_group_permissions'
        unique_together = (('group', 'permission'),)


class AuthPermission(models.Model):
    name = models.CharField(max_length=255)
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING)
    codename = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'auth_permission'
        unique_together = (('content_type', 'codename'),)


class AuthUser(models.Model):
    password = models.CharField(max_length=128)
    last_login = models.DateTimeField(blank=True, null=True)
    is_superuser = models.BooleanField()
    username = models.CharField(unique=True, max_length=150)
    first_name = models.CharField(max_length=150)
    last_name = models.CharField(max_length=150)
    email = models.CharField(max_length=254)
    is_staff = models.BooleanField()
    is_active = models.BooleanField()
    date_joined = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'auth_user'


class AuthUserGroups(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    group = models.ForeignKey(AuthGroup, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_groups'
        unique_together = (('user', 'group'),)


class AuthUserUserPermissions(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)
    permission = models.ForeignKey(AuthPermission, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'auth_user_user_permissions'
        unique_together = (('user', 'permission'),)


class DjangoAdminLog(models.Model):
    action_time = models.DateTimeField()
    object_id = models.TextField(blank=True, null=True)
    object_repr = models.CharField(max_length=200)
    action_flag = models.SmallIntegerField()
    change_message = models.TextField()
    content_type = models.ForeignKey('DjangoContentType', models.DO_NOTHING, blank=True, null=True)
    user = models.ForeignKey(AuthUser, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'django_admin_log'


class DjangoContentType(models.Model):
    app_label = models.CharField(max_length=100)
    model = models.CharField(max_length=100)

    class Meta:
        managed = False
        db_table = 'django_content_type'
        unique_together = (('app_label', 'model'),)


class DjangoMigrations(models.Model):
    id = models.BigAutoField(primary_key=True)
    app = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    applied = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_migrations'


class DjangoSession(models.Model):
    session_key = models.CharField(primary_key=True, max_length=40)
    session_data = models.TextField()
    expire_date = models.DateTimeField()

    class Meta:
        managed = False
        db_table = 'django_session'


class MasterInstruments(models.Model):
    exchangesegment = models.TextField(db_column='ExchangeSegment', blank=True, null=True)  # Field name made lowercase.
    exchangeinstrumentid = models.BigIntegerField(db_column='ExchangeInstrumentID', blank=True, null=True)  # Field name made lowercase.
    instrumenttype = models.BigIntegerField(db_column='InstrumentType', blank=True, null=True)  # Field name made lowercase.
    name = models.TextField(db_column='Name', blank=True, null=True)  # Field name made lowercase.
    description = models.TextField(db_column='Description', blank=True, null=True)  # Field name made lowercase.
    series = models.TextField(db_column='Series', blank=True, null=True)  # Field name made lowercase.
    namewithseries = models.TextField(db_column='NameWithSeries', blank=True, null=True)  # Field name made lowercase.
    instrumentid = models.BigIntegerField(db_column='InstrumentID', blank=True, null=True)  # Field name made lowercase.
    priceband_high = models.FloatField(db_column='PriceBand.High', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    priceband_low = models.FloatField(db_column='PriceBand.Low', blank=True, null=True)  # Field name made lowercase. Field renamed to remove unsuitable characters.
    freezeqty = models.FloatField(db_column='FreezeQty', blank=True, null=True)  # Field name made lowercase.
    ticksize = models.FloatField(db_column='TickSize', blank=True, null=True)  # Field name made lowercase.
    lotsize = models.BigIntegerField(db_column='LotSize', blank=True, null=True)  # Field name made lowercase.
    multiplier = models.BigIntegerField(db_column='Multiplier', blank=True, null=True)  # Field name made lowercase.
    underlyinginstrumentid = models.TextField(db_column='UnderlyingInstrumentId', blank=True, null=True)  # Field name made lowercase.
    underlyingindexname = models.TextField(db_column='UnderlyingIndexName', blank=True, null=True)  # Field name made lowercase.
    contractexpiration = models.TextField(db_column='ContractExpiration', blank=True, null=True)  # Field name made lowercase.
    strikeprice = models.TextField(db_column='StrikePrice', blank=True, null=True)  # Field name made lowercase.
    optiontype = models.TextField(db_column='OptionType', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'master_instruments'


class TradingappMasterinstrument(models.Model):
    id = models.BigAutoField(primary_key=True)
    exchangesegment = models.CharField(db_column='ExchangeSegment', max_length=255)  # Field name made lowercase.
    exchangeinstrumentid = models.CharField(db_column='ExchangeInstrumentID', max_length=255)  # Field name made lowercase.
    instrumenttype = models.CharField(db_column='InstrumentType', max_length=255)  # Field name made lowercase.
    name = models.CharField(db_column='Name', max_length=255)  # Field name made lowercase.
    description = models.TextField(db_column='Description')  # Field name made lowercase.
    series = models.CharField(db_column='Series', max_length=255)  # Field name made lowercase.
    namewithseries = models.CharField(db_column='NameWithSeries', max_length=255)  # Field name made lowercase.
    instrumentid = models.CharField(db_column='InstrumentID', max_length=255)  # Field name made lowercase.
    pricebandhigh = models.FloatField(db_column='PriceBandHigh')  # Field name made lowercase.
    pricebandlow = models.FloatField(db_column='PriceBandLow')  # Field name made lowercase.
    freezeqty = models.IntegerField(db_column='FreezeQty')  # Field name made lowercase.
    ticksize = models.FloatField(db_column='TickSize')  # Field name made lowercase.
    lotsize = models.IntegerField(db_column='LotSize')  # Field name made lowercase.
    multiplier = models.FloatField(db_column='Multiplier')  # Field name made lowercase.
    underlyinginstrumentid = models.CharField(db_column='UnderlyingInstrumentId', max_length=255)  # Field name made lowercase.
    underlyingindexname = models.CharField(db_column='UnderlyingIndexName', max_length=255)  # Field name made lowercase.
    contractexpiration = models.DateField(db_column='ContractExpiration')  # Field name made lowercase.
    strikeprice = models.FloatField(db_column='StrikePrice')  # Field name made lowercase.
    optiontype = models.CharField(db_column='OptionType', max_length=255)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'tradingapp_masterinstrument'
