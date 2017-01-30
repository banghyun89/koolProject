from django.shortcuts import render
from django.http import JsonResponse
from customPackage import sqlCollection
from datetime import datetime, timedelta

#/Users/jihooyim/Library/Python/2.7/lib/python/site-packages

def menu(request):
    return render(request, 'KPLInfo/menu.html')

def getLiveData(request):
    rsList = sqlCollection.get_live_data()
    return JsonResponse({'list': rsList})

def getHistoryData(request):
    v = int(request.GET.get('searchPeriod'))
    rowCnt  = int(request.GET.get('rowCnt'))
    callCnt  = int(request.GET.get('callCnt'))
    firstId = int(request.GET.get('firstId'))
    fromCnt = callCnt * rowCnt
    toCnt = rowCnt

    now = datetime.now()
    timegap = timedelta(days=v)
    before = now - timegap
    todateGap = timedelta(days=2)
    after = now + todateGap

    if v==1:
        fromDate = now.strftime('%Y-%m-%d')
    else :
        fromDate = before.strftime('%Y-%m-%d')

    toDate = after.strftime('%Y-%m-%d')

    param = []
    param.append(fromDate)
    param.append(toDate)
    param.append(firstId)
    param.append(fromCnt)
    param.append(toCnt)

    print('param')
    print(param)
    rsList = sqlCollection.get_history_data(param)


    return JsonResponse({'list': rsList})

def live(request):
    return render(request, 'KPLInfo/live.html')

def history(request):
    return render(request, 'KPLInfo/history.html')
