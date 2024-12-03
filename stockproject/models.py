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


class MasterInstrumentsMarketdata(models.Model):
    id = models.BigAutoField(primary_key=True)
    exchange_segment = models.CharField(max_length=255)
    exchange_instrument_id = models.IntegerField()
    instrument_type = models.CharField(max_length=255)
    name = models.CharField(max_length=255)
    description = models.TextField()
    series = models.CharField(max_length=255)
    name_with_series = models.CharField(max_length=255)
    instrument_id = models.IntegerField()
    price_band_high = models.FloatField()
    price_band_low = models.FloatField()
    freeze_qty = models.FloatField()
    tick_size = models.FloatField()
    lot_size = models.IntegerField()
    multiplier = models.FloatField()
    underlying_instrument_id = models.IntegerField(blank=True, null=True)
    underlying_index_name = models.CharField(max_length=255, blank=True, null=True)
    contract_expiration = models.DateField(blank=True, null=True)
    strike_price = models.FloatField(blank=True, null=True)
    option_type = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'master_instruments.MarketData'
