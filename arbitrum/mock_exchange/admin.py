from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import Asset, PriceTick

@admin.register(Asset)
class AssetAdmin(admin.ModelAdmin):
    list_display = ('ticker', 'name')

@admin.register(PriceTick)
class PriceTickAdmin(admin.ModelAdmin):
    list_display = ('asset', 'price', 'timestamp')
    list_filter = ('asset',)