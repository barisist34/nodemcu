from django.contrib import admin
from .models import Temperature,Device

@admin.register(Temperature)
class TemperatureAdmin(admin.ModelAdmin):
    list_display=[
        'pk',
        'temperature',
        'date',
        'mail',
    ]
@admin.register(Device)
class DeviceAdmin(admin.ModelAdmin):
    list_display=[
        'pk',
        'device_name',
        'device_ip',
        'device_port',
        'device_function',
    ]
