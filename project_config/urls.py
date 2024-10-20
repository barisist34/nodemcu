
from django.contrib import admin
from django.urls import path,include
from app_monitor.views import ilk_def,addRecordArduino,django_device

urlpatterns = [
    path('admin/', admin.site.urls),
    path('app_monitor/',include("app_monitor.urls")),
    path('app_monitor/ilk_def',ilk_def,name="ilk_def"),
    path('addRecordArduino',addRecordArduino,name="addRecordArduino"),


]
