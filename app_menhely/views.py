from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from .filters import AllatFilter
import pprint

# Create your views here.
def bemutatkozas(request):
    bemutatkozoelem = Bemutatkozas.objects.all().order_by('priority')

    return render(request, 'bemutatkozas.html', {'bemutatkozoelem': bemutatkozoelem})
 
def fogadjorokbe(request):
    filtered_animal = AllatFilter(request.GET, queryset=Allat.objects.all())
    paginator = Paginator(filtered_animal.qs, 8)
    print(filtered_animal.qs)

    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'fogadjorokbe.html', {'page_obj': page_obj, 'filtered_animal': filtered_animal})


def allat(request):
    allatid = request.GET.get('allatid')
    allat = Allat.objects.get(id=allatid)
    allatpictures = AllatImage.objects.filter(allat=allat)

    allatok = Allat.objects.exclude(pk = allatid)
    paginator = Paginator(allatok, 6)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    picture_quantity = len(allatpictures)
    breakpnumber = round(picture_quantity/3.)
    breakpremaining = picture_quantity%3
    bplist = [0]
    if breakpremaining in [0,2]:
        bplist.append(breakpnumber)
        bplist.append(2*breakpnumber)
    elif breakpremaining in [1]:
        bplist.append(breakpnumber+1)
        bplist.append(2*breakpnumber+1)


    return render(request, 'allat.html', {'allat': allat, 'allatpictures': allatpictures,'bplist': bplist, 'page_obj': page_obj})


def hir(request):
    hirid = request.GET.get('hirid')
    hir = Hirek.objects.get(id=hirid)
    hirek = Hirek.objects.exclude(pk = hirid)
    paginator = Paginator(hirek, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'hir.html',  {'hir': hir, 'page_obj': page_obj})

def gyik(request):
    return render(request, 'gyik.html', {})
    
def hirek(request):
    hirek = Hirek.objects.all().order_by('-created_at')
    paginator = Paginator(hirek, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'hirek.html', {'page_obj': page_obj})

def help(request):
    return render(request, 'help.html', {})