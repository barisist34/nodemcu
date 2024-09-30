from django.shortcuts import render, HttpResponse,redirect
from .models import Temperature
from django.views.decorators.csrf import csrf_exempt,requires_csrf_token
from django.utils import timezone
from django.core.paginator import Paginator
import django_excel as excel
# from django.http import HttpResponse
from openpyxl import Workbook
from django.db.models import Q


def device_filter_id(request):
    id1=request.GET.get("id1")
    id2=request.GET.get("id2")
    cihazadi=request.GET.get("cihazadi")
    if id1=="" or None:
        filter_result=Temperature.objects.filter(
            id__gte=1,id__lte=id2
            )
    elif id2=="" or None:
        filter_result=Temperature.objects.filter(
            id__gte=id1
            )
    else:
        filter_result=Temperature.objects.filter(
                id__gte=id1,id__lte=id2
                )
    kayit_sayisi_filter=filter_result.count()
    kayit_araligi=f"ID: {id1} -- {id2}"
    print(f"filter_result= {filter_result}")
    print(f"kayıt sayısı filter_result= {kayit_sayisi_filter}")

    paginator = Paginator(filter_result, 5)  # Show 5 contacts per page.
    device_search_count = filter_result.count()
    page_number = request.GET.get('page')
    devicePaginator = paginator.get_page(page_number)
    print(f"devicePaginator: {devicePaginator}")

    context=dict(
        id1=id1,
        id2=id2,
        device_name=cihazadi,
        devicePaginator=devicePaginator,
        kayit_sayisi_filter=kayit_sayisi_filter,
        kayit_araligi=kayit_araligi,
        device500=filter_result,
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
            )       
    elif sicaklik2=="" or None:
        filter_result=Temperature.objects.filter(
                temperature__gte=sicaklik1
                )
    else:
            filter_result=Temperature.objects.filter(
            temperature__gte=sicaklik1,temperature__lte=sicaklik2
            )
    
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
            )
    elif nem2=="" or None:
        filter_result=Temperature.objects.filter(
            humidity__gte=nem1
            )
    else:
        filter_result=Temperature.objects.filter(
                humidity__gte=nem1,humidity__lte=nem2
                )
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
            )
    elif voltaj2=="" or None:
        filter_result=Temperature.objects.filter(
            volcum__gte=voltaj1
            )
    else:
        filter_result=Temperature.objects.filter(
                volcum__gte=voltaj1,volcum__lte=voltaj2
                )
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
            )
    elif tarih2=="" or None:
        filter_result=Temperature.objects.filter(
            date__gte=tarih1
            )
    else:
        filter_result=Temperature.objects.filter(
                date__gte=tarih1,date__lte=tarih2
                )
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


