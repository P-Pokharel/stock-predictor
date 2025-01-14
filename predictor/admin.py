from django.contrib import admin
from .models import StockData

# Register your models here.

@admin.register(StockData)
class StockDataAdmin(admin.ModelAdmin):
    list_display = ('symbol', 'date', 'open_price', 'close_price', 'high', 'low', 'volume', 'percent_change')
    list_filter = ('symbol', 'date')
