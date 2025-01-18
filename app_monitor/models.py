from django.db import models


class Device(models.Model):
    device_id=models.IntegerField(primary_key=True,db_column='ID')
    device_name=models.CharField(blank=True,null=True, max_length=20)
    device_ip=models.CharField(blank=True,null=True, max_length=20)
    device_port=models.IntegerField(blank=True,null=True)
    device_function=models.CharField(blank=True,null=True, max_length=20)
    device_state=models.BooleanField(blank=True,null=True,default=False) #241225
    # device_port1=models.BooleanField(default=False) #241225
    # device_port2=models.BooleanField(default=False) #241225

    def __str__(self):
        return(f"{self.device_id}")

class RFID_Kisi(models.Model):
    id=models.IntegerField(primary_key=True,db_column='ID')
    tag_id=models.CharField(blank=True,null=True, max_length=20)
    staff_name=models.CharField(blank=True,null=True, max_length=30)

    def __str__(self):
        return f"{self.tag_id}"


class RFID_Etiket(models.Model):
    id=models.IntegerField(primary_key=True,db_column='ID')
    tag_id=models.ForeignKey(RFID_Kisi,on_delete=models.CASCADE,null=True,blank=True)
    staff_name=models.CharField(blank=True,null=True, max_length=30)
    cikis3=models.CharField(blank=True,null=True, max_length=5)
    date=models.DateTimeField()

    def __str__(self):
        return f"{self.staff_name}--{self.tag_id}"


class Temperature(models.Model):
    id=models.BigAutoField(primary_key=True,db_column='ID')
    temperature=models.FloatField(blank=True,null=True)
    humidity=models.FloatField(blank=True,null=True)
    volcum=models.FloatField(blank=True,null=True)
    date=models.DateTimeField()
    mail=models.BooleanField(default=False)
    additionalText=models.CharField(blank=True,null=True, max_length=50)
    # device_id=models.IntegerField(blank=True,null=True)
    device_id=models.ForeignKey(Device,on_delete=models.CASCADE,null=True, blank=True)
    device_name=models.CharField(blank=True,null=True, max_length=50)
    cikis1=models.CharField(blank=True,null=True, max_length=5)
    cikis2=models.CharField(blank=True,null=True, max_length=5)
    tag_id=models.ForeignKey(RFID_Kisi,on_delete=models.CASCADE,null=True,blank=True)
    staff_name=models.CharField(blank=True,null=True, max_length=30)
    # device_name=models.ForeignKey(Device,on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return (f"ID:{self.id},Cihaz ID: {self.device_id.device_id} ,Sıcaklık: {self.temperature}, Nem: {self.humidity}, Voltaj: {self.volcum}, Tarih: {self.date}, Cikis1:{self.cikis1}")
    

class Alarm(models.Model):
    id=models.BigAutoField(primary_key=True,db_column='ID')
    alarm_id=models.IntegerField(blank=True,null=True)
    alarm_name=models.CharField(blank=True,null=True, max_length=50)


#Alarmlar: kesinti,port1 down,port2 down,(cihaz bilgisi,saat yok)
#Eventler: kesildi,port1 kesildi (cihaz bilgisi,saat var)

class Event(models.Model):
    id=models.BigAutoField(primary_key=True,db_column='ID')
    device_id=models.ForeignKey(Device,on_delete=models.CASCADE,null=True, blank=True)
    device_name=models.CharField(blank=True,null=True, max_length=50)
    # alarm_id=models.ForeignKey(Alarm,on_delete=models.CASCADE,null=True, blank=True)
    alarm_id=models.IntegerField(blank=True,null=True)
    alarm_name=models.CharField(blank=True,null=True, max_length=50)
    event_active=models.BooleanField(default=True) #alarm devam ediyor mu?  241225
    start_time=models.DateTimeField(blank=True,null=True)
    finish_time=models.DateTimeField(blank=True,null=True)
    info=models.CharField(blank=True,null=True, max_length=50)

    def __str__(self):
        return f"Device name:{self.device_name}--Device ID:{self.device_name}--{self.alarm_name}--{self.start_time}"

