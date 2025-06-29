from django.db import models

# Create your models here.
class ArbitrageOpportunity(models.Model):
    asset = models.CharField(max_length=10)

    exchange_from = models.CharField(max_length=20)
    exchange_to = models.CharField(max_length=20)

    price_from = models.DecimalField(max_digits=10, decimal_places=2)
    price_to = models.DecimalField(max_digits=10, decimal_places=2)

    profit = models.DecimalField(max_digits=10, decimal_places=2)
    profit_percent = models.DecimalField(max_digits=5, decimal_places=2)

    is_active = models.BooleanField(default=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    link_from = models.URLField(blank=True, null=True)
    link_to = models.URLField(blank=True, null=True)
    class Meta:
        unique_together = ("asset", "exchange_from", "exchange_to", "is_active")

    def __str__(self):
        return f"{self.asset}: {self.exchange_from} → {self.exchange_to} ({self.profit}₽)"