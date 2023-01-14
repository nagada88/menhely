from django.shortcuts import render
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from .models import *
from .filters import AllatFilter
import pprint

# Create your views here.
def bemutatkozas(request):
    bemutatkozoelem = Bemutatkozas.objects.all().order_by('priority')
    kapcsolat = Kapcsolat.objects.all()
    
    return render(request, 'bemutatkozas.html', {'bemutatkozoelem': bemutatkozoelem, 'kapcsolat': kapcsolat})
 
def fogadjorokbe(request):
    filtered_animal = AllatFilter(request.GET, queryset=Allat.objects.all().exclude(orokbeadva = True))
    paginator = Paginator(filtered_animal.qs, 8)
    kapcsolat = Kapcsolat.objects.all()
    
    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'fogadjorokbe.html', {'page_obj': page_obj, 'filtered_animal': filtered_animal, 'kapcsolat': kapcsolat})

def orokbefogadott(request):
    animal_number = len(Allat.objects.all().exclude(orokbeadva = False))
    filtered_animal=Allat.objects.all().exclude(orokbeadva = False)
    paginator = Paginator(filtered_animal, 8)
    kapcsolat = Kapcsolat.objects.all()

    page = request.GET.get('page')
    try:
        page_obj = paginator.page(page)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    return render(request, 'orokbefogadott.html', {'page_obj': page_obj, 'filtered_animal': filtered_animal, 'animal_number': animal_number, 'kapcsolat': kapcsolat})



def allat(request):
    allatid = request.GET.get('allatid')
    allat = Allat.objects.get(id=allatid)
    allatpictures = AllatImage.objects.filter(allat=allat)
    kapcsolat = Kapcsolat.objects.all()
    
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


    return render(request, 'allat.html', {'allat': allat, 'allatpictures': allatpictures,'bplist': bplist, 'page_obj': page_obj, 'kapcsolat': kapcsolat})


def hir(request):
    hirid = request.GET.get('hirid')
    hir = Hirek.objects.get(id=hirid)
    hirek = Hirek.objects.exclude(pk = hirid)
    paginator = Paginator(hirek, 3)
    kapcsolat = Kapcsolat.objects.all()
    
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, 'hir.html',  {'hir': hir, 'page_obj': page_obj,'kapcsolat': kapcsolat})

def hirek(request):
    hirek = Hirek.objects.all().order_by('-created_at')
    paginator = Paginator(hirek, 3)

    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    
    kapcsolat = Kapcsolat.objects.all()    
    bemutatkozoelem = Bemutatkozas.objects.all().order_by('priority')
    
    return render(request, 'hirek.html', {'page_obj': page_obj, 'bemutatkozoelem': bemutatkozoelem,'kapcsolat': kapcsolat})

def help(request):
    kapcsolat = Kapcsolat.objects.all()
    return render(request, 'help.html', {'kapcsolat': kapcsolat})