from django.db import models


class Device(models.Model):
    device_id=models.IntegerField(primary_key=True,db_column='ID')
    device_name=models.CharField(blank=True,null=True, max_length=20)
    device_ip=models.CharField(blank=True,null=True, max_length=20)
    device_port=models.IntegerField(blank=True,null=True)
    device_function=models.CharField(blank=True,null=True, max_length=20)

    def __str__(self):
        return(f"{self.device_id}")

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
    # device_name=models.ForeignKey(Device,on_delete=models.CASCADE,null=True, blank=True)

    def __str__(self):
        return (f"ID:{self.id},Sıcaklık: {self.temperature}, Nem: {self.humidity}, Voltaj: {self.volcum}, Tarih: {self.date}")