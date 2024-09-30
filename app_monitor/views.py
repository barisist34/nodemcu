from django.shortcuts import render, HttpResponse,redirect
from .models import Temperature
from django.views.decorators.csrf import csrf_exempt,requires_csrf_token
from django.utils import timezone
from django.core.paginator import Paginator
import django_excel as excel
# from django.http import HttpResponse
from openpyxl import Workbook
from django.db.models import Q

# from django.contrib

# Create your views here.

def ilk_def(request):
    return HttpResponse("Monitor edilecek sayfadasınız...")

def dashboard(request):
    print("dashboard girdi....")
    return render(request,"app_monitor/dashboard.html")

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
        device_id=request.GET.get("device_id")
        print(f"kayit: {kayit} - device_name: {device_name}")
        newRecord = Temperature(temperature=kayit,humidity=humidity ,volcum=volcum,device_name=device_name,device_id=device_id, date=timezone.now())
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
    print(f"son eklenen kayıt: {newRecord.temperature}")
    
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
def deviceView(request,str_device_name):
    deviceAll=Temperature.objects.filter(device_name=str_device_name).order_by('-id')
    device=Temperature.objects.filter(device_name=str_device_name).order_by('-id')[:10]
    device500=Temperature.objects.filter(device_name=str_device_name).order_by('-id')[:500]
    print(f"deviceView girdi, device={str_device_name} ")
    print(f"device çıktısı: , {device} ")
    print(f"str_device_name çıktısı: , {str_device_name} ")
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
    headers = ["device_name","id","temperature", "humidity", "volcum"]
    ws.append(headers)

    # Add data from the model
    if (nem1 or nem2) != "" or None:
        temp = Temperature.objects.filter(device_name__icontains=cihazadi,humidity__gte=nem1,humidity__lte=nem2)
    elif (id1 or id2) != "" or None:
        temp = Temperature.objects.filter(device_name__icontains=cihazadi,id__gte=id1,id__lte=id2)
        print(f"excel id filtre sonuç nesneleri: {temp}")
    else:
        temp = Temperature.objects.filter(device_name__icontains=cihazadi)
    for temps in temp:
        ws.append([temps.device_name,temps.id,temps.temperature, temps.humidity, temps.volcum])

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