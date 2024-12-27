from django.contrib import admin
from .models import Temperature,Device,Alarm,Event

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
@admin.register(Alarm)
class AlarmAdmin(admin.ModelAdmin):
    list_display=[
        'pk',
        'alarm_id',
        'alarm_name',
    ]
@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display=[
        'pk',
        'device_id',
        'device_name',
        'start_time',
        'finish_time',
        'info',
    ]
