from django.db import models

# Create your models here.
class Asset(models.Model):
    ticker = models.CharField(max_length=10, unique=True)
    name = models.CharField(max_length=100)

    def __str__(self):
        return f"{self.ticker} — {self.name}"
    
    
class PriceTick(models.Model):
    asset = models.ForeignKey(Asset, on_delete=models.CASCADE, related_name="ticks")
    timestamp = models.DateTimeField(auto_now_add=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.asset.ticker} @ {self.price} ({self.timestamp})"