from django.db import models


class MasterInstrument(models.Model):
    """
    Represents a master instrument in the database.

    This model stores various attributes related to instruments, such as
    exchange details, pricing, lot size, and underlying information.
    """
    ExchangeSegment = models.CharField(max_length=255, primary_key=True)
    ExchangeInstrumentID = models.CharField(max_length=255)
    InstrumentType = models.CharField(max_length=255)
    Name = models.CharField(max_length=255)
    Description = models.TextField()
    Series = models.CharField(max_length=255)
    NameWithSeries = models.CharField(max_length=255)
    InstrumentID = models.CharField(max_length=255)
    PriceBandHigh = models.FloatField()
    PriceBandLow = models.FloatField()
    FreezeQty = models.IntegerField()
    TickSize = models.FloatField()
    LotSize = models.IntegerField()
    Multiplier = models.FloatField()
    UnderlyingInstrumentId = models.CharField(max_length=255)
    UnderlyingIndexName = models.CharField(max_length=255)
    ContractExpiration = models.DateField()
    StrikePrice = models.FloatField()
    OptionType = models.CharField(max_length=255)

    def __str__(self):
        """Returns a string representation of the model, showing the Name field."""
        return self.Name
    
    class Meta:
        """
        Meta information for the MasterInstrument model.
        """
        managed = False  # Indicates this model is unmanaged by Django migrations.  
        db_table = 'master_instruments'  # Specifies the database table name.