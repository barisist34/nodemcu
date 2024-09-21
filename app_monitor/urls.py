from django.contrib import admin
from django.urls import path
from app_monitor.views import dashboard,TemperatureAddRecord,addRecordArduino,tempList

# app_name="app_monitor"

urlpatterns=[
    path('',dashboard,name="dashboard"),
    # path('<str:str_device_name>',deviceView,name="deviceView"),
    # path('TemperatureAddRecord',TemperatureAddRecord,name="TemperatureAddRecord"),
    path('addRecordArduino',addRecordArduino,name="addRecordArduino"),
    path('tempList',tempList,name="tempList"),

]
