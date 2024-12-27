from django.contrib import admin
from django.urls import path
from app_monitor.views import dashboard,TemperatureAddRecord,addRecordArduino,tempList,deviceView,exportExcel,export_to_excel
from app_monitor.views import django_device,django_device_backtest,deviceViewDetail,export_to_excel_all,devices_all
from app_monitor.views import device_id,export_to_excel_id,arduino_serial_local,additional_text,additional_text_sil,export_to_excel_serial_query
from app_monitor.views import cron_task,scheduler_cihaz,event_list_view,export_to_excel_event_all
from app_monitor.filter import device_filter_id,device_filter_sicaklik,device_filter_nem,device_filter_voltaj,device_filter_tarih

# app_name="app_monitor"

urlpatterns=[
    path('',dashboard,name="dashboard"),
    # path('additional_text/<int:id>/<str:additional_text>',additional_text,name="additional_text"),
    path('additional_text_sil/<int:id>',additional_text_sil,name="additional_text_sil"),
    path('additional_text',additional_text,name="additional_text"),
    path('tempList',tempList,name="tempList"), 
    # path('cihazlar/<str:str_device_name>',deviceView,name="deviceView"), #<str:**> parametresi çok dikkatli kullanılmalı,string oldugu için diğer url leri ezmektedir. Ayrıca cihazlar/ şeklinde bir yol da eklenmelidir.
    path('cihazlar/<str:str_device_name>/port=<int:port_no>',deviceView,name="deviceView"), #<str:**> parametresi çok dikkatli kullanılmalı,string oldugu için diğer url leri ezmektedir. Ayrıca cihazlar/ şeklinde bir yol da eklenmelidir.
    # path('cihazlar/<str:str_device_name>/devid=<int:device_id>/port=<int:port_no>',deviceView,name="deviceView"), #<str:**> parametresi çok dikkatli kullanılmalı,string oldugu için diğer url leri ezmektedir. Ayrıca cihazlar/ şeklinde bir yol da eklenmelidir.
    path('cihazlar/<str:str_device_name>/port=<int:port_no>/devid=<int:device_id>',deviceViewDetail,name="deviceViewDetail"), #<str:**> parametresi çok dikkatli kullanılmalı,string oldugu için diğer url leri ezmektedir. Ayrıca cihazlar/ şeklinde bir yol da eklenmelidir.
    path('cihazlar/<int:device_id>',device_id,name="device_id"),
    path('cihazlar_tum',devices_all,name="devices_all"), #<str:**> parametresi çok dikkatli kullanılmalı,string oldugu için diğer url leri ezmektedir. Ayrıca cihazlar/ şeklinde bir yol da eklenmelidir.

    # path('TemperatureAddRecord',TemperatureAddRecord,name="TemperatureAddRecord"),
    path('addRecordArduino',addRecordArduino,name="addRecordArduino"),
    path('exportExcel',exportExcel,name="exportExcel"),
    path('export_to_excel_serial_query',export_to_excel_serial_query,name="export_to_excel_serial_query"),
    path('export_to_excel',export_to_excel,name="export_to_excel"),
    path('export_to_excel_all',export_to_excel_all,name="export_to_excel_all"),
    path('export_to_excel_id',export_to_excel_id,name="export_to_excel_id"),
    # path('device_filter',device_filter,name="device_filter"),
    path('device_filter_id',device_filter_id,name="device_filter_id"),
    path('device_filter_sicaklik',device_filter_sicaklik,name="device_filter_sicaklik"),
    path('device_filter_nem',device_filter_nem,name="device_filter_nem"),
    path('device_filter_voltaj',device_filter_voltaj,name="device_filter_voltaj"),
    path('device_filter_tarih',device_filter_tarih,name="device_filter_tarih"),
    path('django_device',django_device,name="django_device"),
    path('django_device_backtest',django_device_backtest,name="django_device_backtest"),
    path('arduino_serial_local-<str:config_parameter>',arduino_serial_local,name="arduino_serial_local"),
    path('cron_task',cron_task,name="cron_task"),
    path('scheduler_cihaz',scheduler_cihaz,name="scheduler_cihaz"),
    path('event_list_view',event_list_view,name="event_list_view"),
    path('export_to_excel_event_all',export_to_excel_event_all,name="export_to_excel_event_all"),
    


]
