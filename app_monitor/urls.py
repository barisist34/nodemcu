from django.contrib import admin
from django.urls import path
from app_monitor.views import dashboard,TemperatureAddRecord,addRecordArduino,tempList,deviceView

# app_name="app_monitor"

urlpatterns=[
    path('',dashboard,name="dashboard"),
    path('tempList',tempList,name="tempList"), 
    path('cihazlar/<str:str_device_name>',deviceView,name="deviceView"), #<str:**> parametresi çok dikkatli kullanılmalı,string oldugu için diğer url leri ezmektedir. Ayrıca cihazlar/ şeklinde bir yol da eklenmelidir.
    # path('TemperatureAddRecord',TemperatureAddRecord,name="TemperatureAddRecord"),
    path('addRecordArduino',addRecordArduino,name="addRecordArduino"),

]
