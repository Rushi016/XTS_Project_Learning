from django.db import models

class MarketData(models.Model):
    ExchangeSegment = models.CharField(max_length=255)
    ExchangeInstrumentID = models.CharField(max_length=255)
    InstrumentType = models.CharField(max_length=255)
    Name = models.CharField(max_length=255)
    Description = models.TextField()
    Series = models.CharField(max_length=255)
    NameWithSeries = models.CharField(max_length=255)
    InstrumentID = models.CharField(max_length=255)
    PriceBandHigh = models.DecimalField(max_digits=10, decimal_places=2)
    PriceBandLow = models.DecimalField(max_digits=10, decimal_places=2)
    FreezeQty = models.IntegerField()
    TickSize = models.DecimalField(max_digits=5, decimal_places=2)
    LotSize = models.IntegerField()
    Multiplier = models.DecimalField(max_digits=10, decimal_places=2)
    UnderlyingInstrumentId = models.CharField(max_length=255)
    UnderlyingIndexName = models.CharField(max_length=255)
    ContractExpiration = models.DateField(default='2024-11-27')
    StrikePrice = models.DecimalField(max_digits=10, decimal_places=2)
    OptionType = models.CharField(max_length=255)

    def __str__(self):
        return self.Name
