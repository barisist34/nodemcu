from django.shortcuts import render, HttpResponse,redirect
from .models import Temperature,Device
from django.views.decorators.csrf import csrf_exempt,requires_csrf_token
from django.utils import timezone
from django.core.paginator import Paginator
import django_excel as excel
# from django.http import HttpResponse
from openpyxl import Workbook
from django.db.models import Q
from django.db.models.functions import Lower #241029
from django.conf import settings #241105

# from django.contrib

# Create your views here.

def ilk_def(request):
    return HttpResponse("Monitor edilecek sayfadasınız...")

def dashboard(request):
    print("dashboard girdi....")
    # device_query=Device.objects.all().order_by('device_name')
    device_query=Device.objects.all().order_by(Lower('device_name'))
    context=dict(
        device_query=device_query,
    )
    return render(request,"app_monitor/dashboard.html",context)

# @csrf_exempt
# @requires_csrf_token
def tempList(request):
    tempsajax = Temperature.objects.order_by('-id')[:10]
    kayit_sayisi_total_ajax = Temperature.objects.count()
    print("Templist girdi....")
    context=dict(
        tempsajax=tempsajax,
        kayit_sayisi_total_ajax=kayit_sayisi_total_ajax,
    )
    return render(request, 'app_monitor/temperature_ajax.html', context)

# @csrf_exempt
def TemperatureAddRecord(request): ####RANDOM SICAKLIK, BSC1 tabloları doldurma, form işlemi olmadan, fetchdata_perf() içinde ajax yöntemiyle.

    kayit = request.POST.get("SicaklikKayit")
    newRecord = Temperature(temperature=kayit, date=timezone.now())
    newRecord.save()

    tempsajax = Temperature.objects.order_by('-id')[:10]
    kayit_sayisi_total_ajax = Temperature.objects.count()

    context=dict(
        tempsajax=tempsajax,
        kayit_sayisi_total_ajax=kayit_sayisi_total_ajax,
    )
    return render(request, 'app_monitor/temperature_ajax.html', context)


def addRecordArduino(request): # yeni sıcaklık kaydı ekleme,form get metoduyla
    if request.method == "GET":
        kayit = request.GET.get("kayit")
        humidity = request.GET.get("humidity")
        volcum = request.GET.get("volcum") #voltaj degeri
        device_name=request.GET.get("device_name")
        print(f"Entry.DoesNotExist......??: {Device.objects.filter(device_id=3)}")
        if not Device.objects.filter(device_name__icontains=device_name).exists():
            print(f" {device_name}:  device_id database de olmayan blok girdi... ")
            device_id_request=request.GET.get("device_id")
            device_ip_request=request.GET.get("device_ip")
            device_port_request=request.GET.get("device_port")
            new_device=Device(device_id=device_id_request,device_name=device_name,device_port=device_port_request,device_ip=device_ip_request)
            new_device.save()
            print(f"new_device: {new_device}")
            print(f"new device name: {new_device.device_name}")

        device_id_request=request.GET.get("device_id")
        if not Device.objects.filter(device_id=device_id_request).exists():
            print(f" {device_id_request}:  device_id database de olmayan blok girdi... ")
            # device_id_request=request.GET.get("device_id")
            device_ip_request=request.GET.get("device_ip")
            device_port_request=request.GET.get("device_port")
            new_device=Device(device_id=device_id_request,device_name=device_name,device_port=device_port_request,device_ip=device_ip_request)
            new_device.save()
            print(f"new_device: {new_device}")
            print(f"new device name: {new_device.device_name}")
        
        
        # device_id=Device.objects.get(device_name__icontains=device_name) #241013, device_id Device örneği olmalı, Foreignkey
        device_id_request=request.GET.get("device_id")
        device_id=Device.objects.filter(device_name__icontains=device_name).get(device_id=device_id_request) #241013, device_id Device örneği olmalı, Foreignkey
        
        print(f"kayit: {kayit} - device_name: {device_name}")

        newRecord = Temperature(temperature=kayit,humidity=humidity ,volcum=volcum,device_name=device_name,device_id=device_id, date=timezone.now()) #241013
        newRecord.save()
        # newRecord = Temperature(temperature=kayit,humidity=humidity ,volcum=volcum,device_name=device_name, date=timezone.now())
    else:
        kayit = request.POST.get("kayit")
        if 50<=int(kayit)<=55: # Sıcaklık 50-55 arasında olduğunda mail gönderimi de yapılacaktır.
            newRecord = Temperature(temperature=kayit, date=timezone.now(),mailSend=True)
            email = EmailMessage('Sıcaklık Değeri!', 'Ölçülen Sıcaklık Değeri: ' + f"{kayit}" +' derecedir. \n (50-55 arası sıcaklıklar mail ile bilgilendirilir)', to=['uyarbaris@gmail.com'])
            email.send()
            messages.info(request,f"uyarbaris@gmail.com adresine mail gönderimi yapılmıştır. <br> Sıcaklık:{kayit} ")
        else:
            newRecord = Temperature(temperature=kayit, date=timezone.now())
    newRecord.save()
    print(f"son eklenen sıcaklık: {newRecord.temperature}")
    
    tempsajax = Temperature.objects.order_by('-id')[:10]
    kayit_sayisi_total_ajax = Temperature.objects.count()

    context=dict(
        tempsajax=tempsajax,
        kayit_sayisi_total_ajax=kayit_sayisi_total_ajax,

    )
    # return render(request, 'app_monitor/temperature_ajax.html', context)
    return redirect('/app_monitor')

# GIT commit 240921-2
# @csrf_exempt
# def deviceView(request,str_device_name):
def deviceView(request,str_device_name,port_no):
# def deviceView(request,str_device_name): # parametrelerin sırası ÖNEMLİ
    deviceAll=Temperature.objects.filter(device_name=str_device_name).order_by('-id')
    device=Temperature.objects.filter(device_name=str_device_name).order_by('-id')[:10]
    # device500=Temperature.objects.filter(device_name=str_device_name).order_by('-id')[:500]
    device500=Temperature.objects.filter(device_name=str_device_name).order_by('-id')[:500]
    # device_port=Device.objects.get(device_name=str_device_name).device_port
    device_port=port_no
    print(f"deviceView girdi, device={str_device_name} ")
    print(f"device çıktısı: , {device} ")
    print(f"str_device_name çıktısı: , {str_device_name} ")
    print(f"port no url parametre: , {port_no} ")
    paginator = Paginator(deviceAll, 5)  # Show 5 contacts per page.

    device_search_count = deviceAll.count()

    page_number = request.GET.get('page')

    devicePaginator = paginator.get_page(page_number)

    context=dict(
        device=device,
        device_name=str_device_name.lower(),
        device500=device500,
        devicePaginator=devicePaginator,
        device_search_count=device_search_count,
        device_port=device_port,
    )
    return render(request,"app_monitor/device.html",context)


def deviceViewDetail(request,str_device_name,port_no,device_id): # parametrelerin sırası ÖNEMLİ
    deviceAll=Temperature.objects.filter(device_name=str_device_name).filter(device_id=device_id).order_by('-id')
    device=Temperature.objects.filter(device_name=str_device_name).filter(device_id=device_id).order_by('-id')[:10]
    # device500=Temperature.objects.filter(device_name=str_device_name).order_by('-id')[:500]
    device500=Temperature.objects.filter(device_name=str_device_name).filter(device_id=device_id).order_by('-id')[:50]
    # device_port=Device.objects.get(device_name=str_device_name).device_port
    device_port=port_no
    print(f"deviceView girdi, device={str_device_name} ")
    print(f"device çıktısı: , {device} ")
    print(f"str_device_name çıktısı: , {str_device_name} ")
    print(f"port no url parametre: , {port_no} ")
    paginator = Paginator(deviceAll, 5)  # Show 5 contacts per page.

    device_search_count = deviceAll.count()

    page_number = request.GET.get('page')

    devicePaginator = paginator.get_page(page_number)

    context=dict(
        device=device,
        device_name=str_device_name.lower(),
        device500=device500,
        devicePaginator=devicePaginator,
        device_search_count=device_search_count,
        device_port=device_port,
    )
    return render(request,"app_monitor/device.html",context)

#Excel export
def exportExcel(request):
    temps10=Temperature.objects.order_by('-id')[:10]
    
    return excel.make_response_from_a_table(Temperature, "xls", file_name="sheet")

#Excel export 2
def export_to_excel(request):
    cihazadi=request.GET.get("cihazadi")
    id1=request.GET.get("id1")
    id2=request.GET.get("id2")
    nem1=request.GET.get("nem1")
    nem2=request.GET.get("nem2")
    print(f"cihazadi export_to_excel= {cihazadi}")
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{cihazadi}.xlsx"'

    wb = Workbook()
    ws = wb.active
    ws.title = cihazadi

    # Add headers
    headers = ["id","DEVICE NAME","DEVICE ID","DEVICE PORT","temperature", "humidity", "volcum"]
    ws.append(headers)

    # Add data from the model
    if (nem1 or nem2) != "" or None:
        # temp = Temperature.objects.filter(device_name__icontains=cihazadi,humidity__gte=nem1,humidity__lte=nem2)
        temp = Temperature.objects.filter(device_name=cihazadi,humidity__gte=nem1,humidity__lte=nem2)
    elif (id1 or id2) != "" or None:
        temp = Temperature.objects.filter(device_name=cihazadi,id__gte=id1,id__lte=id2)
        print(f"excel id filtre sonuç nesneleri: {temp}")
    else:
        # temp = Temperature.objects.filter(device_name__icontains=cihazadi)
        temp = Temperature.objects.filter(device_name__iexact=cihazadi) #iexact kullanıldı exact değil
        # temp = Temperature.objects.filter(device_name=cihazadi)
    for temps in temp:
        ws.append([temps.id,temps.device_name,temps.device_id.device_id,temps.device_id.device_port,temps.temperature, temps.humidity, temps.volcum])

    # Save the workbook to the HttpResponse
    wb.save(response)
    return response

#Excel export ALL
def export_to_excel_all(request):
    # cihazadi=request.GET.get("cihazadi")
    # id1=request.GET.get("id1")
    # id2=request.GET.get("id2")
    # nem1=request.GET.get("nem1")
    # nem2=request.GET.get("nem2")
    # print(f"cihazadi export_to_excel= {cihazadi}")
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="ALL.xlsx"'

    wb = Workbook()
    ws = wb.active
    ws.title = "ALL"

    # Add headers
    headers = ["id","DEVICE NAME","DEVICE ID","DEVICE PORT","temperature", "humidity", "volcum"]
    ws.append(headers)


    temp = Temperature.objects.all() 
        # temp = Temperature.objects.filter(device_name=cihazadi)
    for temps in temp:
        try:
            ws.append([temps.id,temps.device_name,temps.device_id.device_id,temps.device_id.device_port,temps.temperature, temps.humidity, temps.volcum])
            # ws.append([temps.id,temps.device_name,temps.temperature, temps.humidity, temps.volcum])
        except AttributeError:
            print("AttributeError oluştu...")

    # Save the workbook to the HttpResponse
    wb.save(response)
    return response


def export_to_excel_nem(request):
    nem1=request.GET.get("nem1")
    nem2=request.GET.get("nem2")
    cihazadi=request.GET.get("cihazadi")
    print(f"cihazadi= {cihazadi}")
    response = HttpResponse(content_type='application/ms-excel')
    response['Content-Disposition'] = f'attachment; filename="{cihazadi}.xlsx"'
    wb = Workbook()
    ws = wb.active
    ws.title = cihazadi
    headers = ["device_name","id","temperature", "humidity", "volcum"]
    ws.append(headers)
    temp = Temperature.objects.filter(device_name__icontains=cihazadi,humidity__gte=nem1,humidity__lte=nem2)
    for temps in temp:
        ws.append([temps.device_name,temps.id,temps.temperature, temps.humidity, temps.volcum])
    wb.save(response)
    return response

def django_device(request):
    device_ip = request.GET.get("device_ip")
    device_port=request.GET.get("name-port")
    print(f"django_device girdi: {device_ip}")
    devices_all=Device.objects.all()
    cihazlar_erisim_ip=settings.CIHAZLAR_ERISIM_IP

    context=dict(
        device_ip=device_ip,
        device_port=device_port,
        devices_all=devices_all,
        cihazlar_erisim_ip=cihazlar_erisim_ip,
    )

    return render(request,"app_monitor/django_arduino.html",context)

def django_device_backtest(request):
    device_ip = request.GET.get("device_ip")
    print(f"DJANGO BACKTEST girdi: {device_ip}")
    return HttpResponse(device_ip)

def devices_all(request):
    devices_all=Device.objects.all()
    context=dict(
        devices_all=devices_all,

    )
    return render(request,"app_monitor/devices_all.html",context)

#241104 github commit test