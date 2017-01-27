from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.
from django.http import JsonResponse
#from .models import Obd
from customPackage import sqlCollection
from datetime import datetime, timedelta

#/Users/jihooyim/Library/Python/2.7/lib/python/site-packages

def menu(request):
    return render(request, 'KPLInfo/menu.html')

def getLiveData(request):

    rs = sqlCollection.get_live_data()
    return JsonResponse({'realFuelValue': rs, 'avgFuelValue':rs})

def getHistoryData(request):
    v = int(request.GET.get('searchPeriod'))

    now = datetime.now()
    timegap = timedelta(days=v)
    before = now - timegap
    todateGap = timedelta(days=1)
    after = now + todateGap

    if v==1:
        fromDate = now.strftime('%Y-%m-%d')
    else :
        fromDate = before.strftime('%Y-%m-%d')
    toDate = after.strftime('%Y-%m-%d')
    param = []
    param.append(fromDate)
    param.append(toDate)
    rsList = sqlCollection.get_history_data(param)

    return JsonResponse({'list': rsList})

def live(request):
    return render(request, 'KPLInfo/live.html')

def history(request):
    return render(request, 'KPLInfo/history.html')
