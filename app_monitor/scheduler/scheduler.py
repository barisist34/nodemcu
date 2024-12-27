from apscheduler.schedulers.background import BackgroundScheduler,BlockingScheduler
from django_apscheduler.jobstores import DjangoJobStore, register_events
from django.utils import timezone
from django_apscheduler.models import DjangoJobExecution
from app_monitor.views import scheduler_cihaz
import sys
from app_monitor.views import Device,Event
from datetime import datetime

# This is the function you want to schedule - add as many as you want and then register them in the start() function below
def first_task_view():
    today = timezone.now()

    ...
    print(f"first_task_view başladı,20 saniyede bir tekrarlar: {today}")
    # scheduler_cihaz(request)
    # get accounts, expire them, etc.
    ...
   #event create yapılmalı,daha önce cihazın ilgili durumuyla ilgili event yoksa
    #aşağıda aktif eventler düzelip düzelmedikleri kontrol edilmelidir.
    #EVENT oluşturma:    
    datetime_now=datetime.now()

    devices_all=Device.objects.all()
    for device in devices_all:
        if device.event_set.last() is None:
            if (datetime.timestamp(datetime_now) - datetime.timestamp(device.temperature_set.last().date) > 360):# and (device.event_set.last().event_active==False): #saha kesikse ve event en son aktif değilse(saha çalışıyorsa),yeni event ekle.
                device.device_state=False
                new_event=Event(device_id=device,device_name=device.device_name,alarm_id=1,alarm_name="Cihaz Kesik",start_time=datetime_now)
                new_event.save()
                print(f"(device.event_set.last().event_active):{device.event_set.last().event_active}")
            # else:
            #     if (datetime.timestamp(datetime_now) - datetime.timestamp(device.temperature_set.last().date) > 360) and (device.event_set.last().event_active==False): #saha kesikse ve event en son aktif değilse(saha çalışıyorsa),yeni event ekle.
            #         device.device_state=False
            #         new_event=Event(device_id=device,device_name=device.device_name,alarm_id=1,alarm_name="Cihaz Kesik",start_time=datetime_now)
            #         new_event.save()
            #         print(f"(device.event_set.last().event_active):{device.event_set.last().event_active}")
            
        else:
            if (datetime.timestamp(datetime_now) - datetime.timestamp(device.temperature_set.last().date) > 360) and (device.event_set.last().event_active==False): #saha kesikse ve event en son aktif değilse(saha çalışıyorsa),yeni event ekle.
                device.device_state=False
                new_event=Event(device_id=device,device_name=device.device_name,alarm_id=1,alarm_name="Cihaz Kesik",start_time=datetime_now)
                new_event.save()
                print(f"(device.event_set.last().event_active):{device.event_set.last().event_active}")

    events=Event.objects.all()
    # print(f"events: {events}")
    #EVENT clear yapma:
    for event in events:
    # for device in devices_all:
        if datetime.timestamp(datetime_now) - datetime.timestamp(event.device_id.temperature_set.last().date) < 360: #gerçekte online ise
            print("event clear bloğuna girdi...")
            device_state_now=True
            if event.event_active == True: #event devam ediyorsa
                event.event_active=False #event düzeldi yap
                event.finish_time=datetime.now()
                event.save()
            else:
                pass # event olarak devam etmiyorsa


def start():
    scheduler = BackgroundScheduler() # 2 defa aynı job çalışıyor,yani düzensiz. start tan sonraki print server ilk başlayınca yazdırılıyor sadece. 
    # scheduler = BlockingScheduler() # normal çalışıyor,start sonrası print bloke ediliyor,hiç yazdırılmıyor. Server çalışmasını bloke ediyor,sadece kendi taskı çalışıyor.
    # scheduler.add_jobstore(DjangoJobStore(), "default") # bu komut olursa çoklu defa düzensiz çalışıyor.
    # run this job every 24 hours
    # scheduler.add_job(first_task_view, 'interval', hours=24, name='clean_accounts', jobstore='default')
    job=scheduler.add_job(first_task_view, 'interval', seconds=30, name='clean_accounts', jobstore='default')
    # job=scheduler.add_job(scheduler_cihaz, 'interval', seconds=30, name='clean_accounts', jobstore='default')
    # register_events(scheduler)
    scheduler.start()
    # job.remove()
    print("blocking yada backgroundscheduler kontrolu...")
    print("Scheduler started...", file=sys.stdout)