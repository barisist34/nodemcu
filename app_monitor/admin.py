from django.contrib import admin
from .models import Temperature

@admin.register(Temperature)
class TemperatureAdmin(admin.ModelAdmin):
    list_display=[
        'pk',
        'temperature',
        'date',
        'mail',
    ]
