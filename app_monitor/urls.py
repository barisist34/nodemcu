from django.contrib import admin
from django.urls import path
from app_monitor.views import dashboard,TemperatureAddRecord,addRecordArduino,tempList,deviceView,exportExcel,export_to_excel
from app_monitor.filter import device_filter_id,device_filter_sicaklik,device_filter_nem,device_filter_voltaj,device_filter_tarih

# app_name="app_monitor"

urlpatterns=[
    path('',dashboard,name="dashboard"),
    path('tempList',tempList,name="tempList"), 
    path('cihazlar/<str:str_device_name>',deviceView,name="deviceView"), #<str:**> parametresi çok dikkatli kullanılmalı,string oldugu için diğer url leri ezmektedir. Ayrıca cihazlar/ şeklinde bir yol da eklenmelidir.
    # path('TemperatureAddRecord',TemperatureAddRecord,name="TemperatureAddRecord"),
    path('addRecordArduino',addRecordArduino,name="addRecordArduino"),
    path('exportExcel',exportExcel,name="exportExcel"),
    path('export_to_excel',export_to_excel,name="export_to_excel"),
    # path('device_filter',device_filter,name="device_filter"),
    path('device_filter_id',device_filter_id,name="device_filter_id"),
    path('device_filter_sicaklik',device_filter_sicaklik,name="device_filter_sicaklik"),
    path('device_filter_nem',device_filter_nem,name="device_filter_nem"),
    path('device_filter_voltaj',device_filter_voltaj,name="device_filter_voltaj"),
    path('device_filter_tarih',device_filter_tarih,name="device_filter_tarih"),

]
