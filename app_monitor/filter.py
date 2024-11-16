from django.shortcuts import render, HttpResponse,redirect
from .models import Temperature
from django.views.decorators.csrf import csrf_exempt,requires_csrf_token
from django.utils import timezone
from django.core.paginator import Paginator
import django_excel as excel
# from django.http import HttpResponse
from openpyxl import Workbook
from django.db.models import Q
from datetime import datetime


def device_filter_id(request):
    id1=request.GET.get("id1")
    id2=request.GET.get("id2")
    sicaklik1=request.GET.get("sicaklik1")
    sicaklik2=request.GET.get("sicaklik2")
    nem1=request.GET.get("nem1")
    nem2=request.GET.get("nem2")
    voltaj1=request.GET.get("voltaj1")
    voltaj2=request.GET.get("voltaj2")
    tarih1=request.GET.get("tarih1")
    tarih2=request.GET.get("tarih2")   
    cihazadi=request.GET.get("cihazadi")

    #ID aralığı
    if (id1=="" or None) and (id2=="" or None):
        filter_result_id=Temperature.objects.filter(
            id__gte=1,id__lte=Temperature.objects.last().id
            ).filter(device_name=cihazadi.capitalize()).order_by('-id')
        print(f"(id1=='' or None) and (id2=="" or None)")
    elif id1=="" or None: 
        filter_result_id=Temperature.objects.filter(
            id__gte=1,id__lte=id2
            ).filter(device_name=cihazadi.capitalize()).order_by('-id')
        print(f"id1=='' or None")
    elif id2=="" or None:
        filter_result_id=Temperature.objects.filter(
            id__gte=id1
            ).filter(device_name=cihazadi.capitalize()).order_by('-id')
        print(f"id2=='' or None")
    
    else:
        filter_result_id=Temperature.objects.filter(
                id__gte=id1,id__lte=id2
                ).filter(device_name=cihazadi.capitalize()).order_by('-id')
        print(f"id__gte=id1,id__lte=id2")
        print(f"id sayısı: {filter_result_id.count()}")
    
    #SICAKLIK aralığı
    if (sicaklik1=="" or None) and (sicaklik2=="" or None): 
            filter_result_temp=filter_result_id.filter(
            # temperature__gte=0,temperature__lte=sicaklik2
            temperature__gte=0,temperature__lte=100
            ).filter(device_name=cihazadi.capitalize()).order_by('-id')  
            print(f"sicaklik kontrolu: sicaklik1=='' or None and sicaklik2=='' or None")  
            print(f"temp sayısı none-none: {filter_result_temp.count()}")   
    elif sicaklik1=="" or None: #SICAKLIK aralığı
            filter_result_temp=filter_result_id.filter(
            # temperature__gte=0,temperature__lte=sicaklik2
            temperature__gte=0,temperature__lte=sicaklik2
            ).filter(device_name=cihazadi.capitalize()).order_by('-id')       
    elif sicaklik2=="" or None:
        filter_result_temp=filter_result_id.filter(
                temperature__gte=sicaklik1
                ).filter(device_name=cihazadi.capitalize()).order_by('-id')
    else:
            filter_result_temp=filter_result_id.filter(
            temperature__gte=sicaklik1,temperature__lte=sicaklik2
            ).filter(device_name=cihazadi.capitalize()).order_by('-id')
    #NEM aralığı
    if (nem1=="" or None) and (nem2=="" or None): 
        filter_result_nem=filter_result_temp.filter(
            humidity__gte=0,humidity__lte=100
            ).filter(device_name=cihazadi.capitalize()).order_by('-id')
        print(f"nem kontrolu:nem1=="" or None) and (nem2=="" or None ")
        print(f"nem sayısı none-none: {filter_result_nem.count()}") 
    elif nem1=="" or None: 
        filter_result_nem=filter_result_temp.filter(
            humidity__gte=0,humidity__lte=nem2
            ).filter(device_name=cihazadi.capitalize()).order_by('-id')
    elif nem2=="" or None:
        filter_result_nem=filter_result_temp.filter(
            humidity__gte=nem1
            ).filter(device_name=cihazadi.capitalize()).order_by('-id')
    else:
        filter_result_nem=filter_result_temp.filter(
                humidity__gte=nem1,humidity__lte=nem2
                ).filter(device_name=cihazadi.capitalize()).order_by('-id')  
        print(f"nem kontrolu:humidity__gte=nem1,humidity__lte=nem2") 
        print(f"nem sayısı nem1-nem2: {filter_result_nem.count()}")  
    #VOLTAJ aralığı
    if (voltaj1=="" or None) and (voltaj2=="" or None): 
        filter_result_voltaj=filter_result_nem.filter(
            volcum__gte=0,volcum__lte=20
            ).filter(device_name=cihazadi.capitalize()).order_by('-id')
        print(f"voltaj kontrolu:voltaj1=="" or None) and (voltaj2=="" or None ")
        print(f"voltaj sayısı none-none: {filter_result_voltaj.count()}") 
    elif voltaj1=="" or None: 
        filter_result_voltaj=filter_result_nem.filter(
            volcum__gte=0,volcum__lte=voltaj2
            ).filter(device_name=cihazadi.capitalize()).order_by('-id')
    elif voltaj2=="" or None:
        filter_result_voltaj=filter_result_nem.filter(
            volcum__gte=voltaj1
            ).filter(device_name=cihazadi.capitalize()).order_by('-id')
    else:
        filter_result_voltaj=filter_result_nem.filter(
                volcum__gte=voltaj1,volcum__lte=voltaj2
                ).filter(device_name=cihazadi.capitalize()).order_by('-id')    
        print(f"voltaj sayısı: {filter_result_voltaj.count()}")
        print(f"nem sayısı: {filter_result_nem.count()}")

    #TARIH aralığı
    print(f"tarih1 tipi: {type(tarih1)}")
    print(f"tarih1: {tarih1}")
    #2024-11-12 22:40:06.395707   '%Y-'
    tarih1_datetime=datetime.strptime(tarih1,'%Y-%m-%dT%H:%M') #string-datetime
    tarih1=datetime.strftime(tarih1_datetime,'%Y-%m-%d %H:%M') #datetime format değiştirme
    tarih2_datetime=datetime.strptime(tarih2,'%Y-%m-%dT%H:%M') #string-datetime
    tarih2=datetime.strftime(tarih2_datetime,'%Y-%m-%d %H:%M') #datetime format değiştirme
    # tarih1_datetime=datetime.date(tarih1)
    # print(f"tarih1_datetime tipi: {type(tarih1_datetime)}")
    if (tarih1=="" or None) and (tarih2=="" or None): 
        filter_result_tarih=filter_result_voltaj.filter(
            date__gte=datetime(2023,12,30),date__lte=datetime.now()
            ).filter(device_name=cihazadi.capitalize()).order_by('-id')
        print(f"tarih kontrolu:tarih1=="" or None) and (tarih2=="" or None ")
        print(f"tarih sayısı none-none: {filter_result_tarih.count()}") 
    elif tarih1=="" or None: 
        filter_result_tarih=filter_result_voltaj.filter(
            date__lte=tarih2
            ).filter(device_name=cihazadi.capitalize()).order_by('-id')
    elif tarih2=="" or None:
        filter_result_tarih=filter_result_voltaj.filter(
            date__gte=tarih1
            ).filter(device_name=cihazadi.capitalize()).order_by('-id')
    else:
        filter_result_tarih=filter_result_voltaj.filter(
                date__gte=tarih1,date__lte=tarih2
                ).filter(device_name=cihazadi.capitalize()).order_by('-id')    
        print(f"tarih sayısı: {filter_result_tarih.count()}")
        print(f"voltaj sayısı: {filter_result_voltaj.count()}")
    
    kayit_sayisi_filter=filter_result_tarih.count()
    kayit_araligi=f"ID: {id1} -- {id2}"
    # print(f"filter_result= {filter_result_nem}")
    # print(f"kayıt sayısı filter_result= {kayit_sayisi_filter}")

    paginator = Paginator(filter_result_voltaj, 5)  # Show 5 contacts per page.
    device_search_count = filter_result_voltaj.count()
    page_number = request.GET.get('page')
    devicePaginator = paginator.get_page(page_number)
    print(f"devicePaginator: {devicePaginator}")

    context=dict(
        id1=id1,
        id2=id2,
        sicaklik1=sicaklik1,
        sicaklik2=sicaklik2,
        nem1=nem1,
        nem2=nem2,
        voltaj1=voltaj1,
        voltaj2=voltaj2,
        tarih1=tarih1,
        tarih2=tarih2,
        device_name=cihazadi,
        devicePaginator=devicePaginator,
        kayit_sayisi_filter=kayit_sayisi_filter,
        kayit_araligi=kayit_araligi,
        device500=filter_result_temp,
        graph_adi="ID",
    )
    # return HttpResponse(filter_result)
    return render (request,"app_monitor/device.html",context)

def device_filter_sicaklik(request):
    sicaklik1=request.GET.get("sicaklik1")
    sicaklik2=request.GET.get("sicaklik2")
    cihazadi=request.GET.get("cihazadi")

    if sicaklik1=="" or None:
            filter_result=Temperature.objects.filter(
            temperature__gte=0,temperature__lte=sicaklik2
            ).filter(device_name=cihazadi.capitalize()).order_by('-id')       
    elif sicaklik2=="" or None:
        filter_result=Temperature.objects.filter(
                temperature__gte=sicaklik1
                ).filter(device_name=cihazadi.capitalize()).order_by('-id')
    else:
            filter_result=Temperature.objects.filter(
            temperature__gte=sicaklik1,temperature__lte=sicaklik2
            ).filter(device_name=cihazadi.capitalize()).order_by('-id')
    
    print(f"filter_result= {filter_result}")
    kayit_sayisi_filter=filter_result.count()
    kayit_araligi=f"Sıcaklık: {sicaklik1} -- {sicaklik2}"
    print(f"kayıt sayısı filter_result= {kayit_sayisi_filter}")

    paginator = Paginator(filter_result, 5)  # Show 5 contacts per page.
    device_search_count = filter_result.count()
    page_number = request.GET.get('page')
    devicePaginator = paginator.get_page(page_number)
    print(f"devicePaginator: {devicePaginator}")

    context=dict(
        sicaklik1=sicaklik1,
        sicaklik2=sicaklik2,
        device_name=cihazadi,
        devicePaginator=devicePaginator,
        kayit_sayisi_filter=kayit_sayisi_filter,
        kayit_araligi=kayit_araligi,
        device500=filter_result,
        graph_adi="ID",
    )
    # return HttpResponse(filter_result)
    return render (request,"app_monitor/device.html",context)

def device_filter_nem(request):
    nem1=request.GET.get("nem1")
    nem2=request.GET.get("nem2")
    cihazadi=request.GET.get("cihazadi")

    if nem1=="" or None:
        filter_result=Temperature.objects.filter(
            humidity__gte=0,humidity__lte=nem2
            ).filter(device_name=cihazadi.capitalize()).order_by('-id')
    elif nem2=="" or None:
        filter_result=Temperature.objects.filter(
            humidity__gte=nem1
            ).filter(device_name=cihazadi.capitalize()).order_by('-id')
    else:
        filter_result=Temperature.objects.filter(
                humidity__gte=nem1,humidity__lte=nem2
                ).filter(device_name=cihazadi.capitalize()).order_by('-id')
    kayit_sayisi_filter=filter_result.count()
    kayit_araligi=f"Nem: {nem1} -- {nem2}"
    print(f"filter_result= {filter_result}")
    print(f"kayıt sayısı filter_result= {kayit_sayisi_filter}")

    paginator = Paginator(filter_result, 5)  # Show 5 contacts per page.
    device_search_count = filter_result.count()
    page_number = request.GET.get('page')
    devicePaginator = paginator.get_page(page_number)
    print(f"devicePaginator: {devicePaginator}")

    context=dict(
        nem1=nem1,
        nem2=nem2,
        device_name=cihazadi,
        devicePaginator=devicePaginator,
        kayit_sayisi_filter=kayit_sayisi_filter,
        kayit_araligi=kayit_araligi,
        device500=filter_result,
    )
    # return HttpResponse(filter_result)
    return render (request,"app_monitor/device.html",context)

def device_filter_voltaj(request):
    voltaj1=request.GET.get("voltaj1")
    voltaj2=request.GET.get("voltaj2")
    cihazadi=request.GET.get("cihazadi")
    if voltaj1=="" or None:
        filter_result=Temperature.objects.filter(
            volcum__gte=0,volcum__lte=voltaj2
            ).filter(device_name=cihazadi.capitalize()).order_by('-id')
    elif voltaj2=="" or None:
        filter_result=Temperature.objects.filter(
            volcum__gte=voltaj1
            ).filter(device_name=cihazadi.capitalize()).order_by('-id')
    else:
        filter_result=Temperature.objects.filter(
                volcum__gte=voltaj1,volcum__lte=voltaj2
                ).filter(device_name=cihazadi.capitalize()).order_by('-id')
    kayit_sayisi_filter=filter_result.count()
    kayit_araligi=f"Voltaj: {voltaj1} -- {voltaj2}"
    print(f"filter_result= {filter_result}")
    print(f"kayıt sayısı filter_result= {kayit_sayisi_filter}")

    paginator = Paginator(filter_result, 5)  # Show 5 contacts per page.
    device_search_count = filter_result.count()
    page_number = request.GET.get('page')
    devicePaginator = paginator.get_page(page_number)
    print(f"devicePaginator: {devicePaginator}")

    context=dict(
        voltaj1=voltaj1,
        voltaj2=voltaj2,
        device_name=cihazadi,
        devicePaginator=devicePaginator,
        kayit_sayisi_filter=kayit_sayisi_filter,
        kayit_araligi=kayit_araligi,
        device500=filter_result,
    )
    # return HttpResponse(filter_result)
    return render (request,"app_monitor/device.html",context)



def device_filter_tarih(request):
    tarih1=request.GET.get("tarih1")
    tarih2=request.GET.get("tarih2")
    cihazadi=request.GET.get("cihazadi")

    if tarih1=="" or None:
        filter_result=Temperature.objects.filter(
            date__lte=tarih2
            ).filter(device_name=cihazadi.capitalize()).order_by('-id')
    elif tarih2=="" or None:
        filter_result=Temperature.objects.filter(
            date__gte=tarih1
            ).filter(device_name=cihazadi.capitalize()).order_by('-id')
    else:
        filter_result=Temperature.objects.filter(
                date__gte=tarih1,date__lte=tarih2
                ).filter(device_name=cihazadi.capitalize()).order_by('-id')
    kayit_sayisi_filter=filter_result.count()
    kayit_araligi=f"Tarih: {tarih1} -- {tarih2}"
    print(f"filter_result= {filter_result}")
    print(f"kayıt sayısı filter_result= {kayit_sayisi_filter}")

    paginator = Paginator(filter_result, 5)  # Show 5 contacts per page.
    device_search_count = filter_result.count()
    page_number = request.GET.get('page')
    devicePaginator = paginator.get_page(page_number)
    print(f"devicePaginator: {devicePaginator}")

    context=dict(
        tarih1=tarih1,
        tarih2=tarih2,
        device_name=cihazadi,
        devicePaginator=devicePaginator,
        kayit_sayisi_filter=kayit_sayisi_filter,
        kayit_araligi=kayit_araligi,
        device500=filter_result,
    )
    # return HttpResponse(filter_result)
    return render (request,"app_monitor/device.html",context)


