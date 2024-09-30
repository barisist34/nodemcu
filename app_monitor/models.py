from django.db import models


class Temperature(models.Model):
    id=models.BigAutoField(primary_key=True,db_column='ID')
    temperature=models.FloatField(blank=True,null=True)
    humidity=models.FloatField(blank=True,null=True)
    volcum=models.FloatField(blank=True,null=True)
    date=models.DateTimeField()
    mail=models.BooleanField(default=False)
    additionalText=models.CharField(blank=True,null=True, max_length=50)
    device_id=models.IntegerField(blank=True,null=True)
    device_name=models.CharField(blank=True,null=True, max_length=50)

    def __str__(self):
        return (f"ID:{self.id},Sıcaklık: {self.temperature}, Nem: {self.humidity}, Voltaj: {self.volcum}, Tarih: {self.date}")