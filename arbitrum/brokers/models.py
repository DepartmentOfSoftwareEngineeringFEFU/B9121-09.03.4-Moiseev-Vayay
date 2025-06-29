from django.db import models

# Create your models here.
class Exchange(models.Model):
    name = models.CharField(max_length=100)
    code = models.CharField(max_length=20)
    api_url = models.URLField(blank=True, null=True)
   # commission = models.DecimalField(max_digits=5, decimal_places=2, default=0.0)

    def __str__(self):
        return self.name
    
    
    
    
class Tariff(models.Model):
    exchange = models.ForeignKey(
        Exchange,
        on_delete=models.CASCADE,
        related_name='tariffs',
        verbose_name="Биржа"
    )
    name = models.CharField(max_length=100, verbose_name="Название тарифа")
    commission = models.DecimalField(
        max_digits=5,
        decimal_places=2,
        verbose_name="Комиссия (%)"
    )

    def __str__(self):
        return f"{self.exchange.name} — {self.name} ({self.commission}%)"
    
    # onlu tinkoff assets актива
class AssetTinkoff(models.Model):
    ticker = models.CharField(max_length=20)
    figi = models.CharField(max_length=50, unique=True)
    class_code = models.CharField(max_length=20)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.ticker} ({self.name})"
#название актива
# class Asset(models.Model):
#     symbol = models.CharField(max_length=20)
#     name = models.CharField(max_length=100)

#     def __str__(self):
#         return self.symbol
    
#  #цена актива на бирже в момент времени
# class Quote(models.Model):
#     exchange = models.ForeignKey(Exchange, on_delete=models.CASCADE)
#     asset = models.ForeignKey(Asset, on_delete=models.CASCADE)
#     price = models.DecimalField(max_digits=20, decimal_places=6)
#     timestamp = models.DateTimeField(auto_now_add=True)

#     def __str__(self):
#         return f"{self.asset.symbol} @ {self.exchange.name} = {self.price}"