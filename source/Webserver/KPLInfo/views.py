from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from .models import Obd


def menu(request):
    return render(request, 'KPLInfo/menu.html')

def live(request):
    afv = "14.0";
    row = Obd.objects.order_by('time').last()
    rfv = row.kpl
    return render(request, 'KPLInfo/live.html', {'realFuelValue':rfv,'avgFuelValue':afv})


def history(request):
    return render(request, 'KPLInfo/history.html')

#def requestHistoryData(request):


#def requestLiveData(request):