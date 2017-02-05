import sys
sys.path.append("..")
from django.shortcuts import render
from django.http import JsonResponse
from dbConn import sqlCollection
from datetime import datetime, timedelta

def menu(request):
    return render(request, 'templates/menu.html')

def getLiveData(request):
    rsList = sqlCollection.get_live_data()
    return JsonResponse(rsList)

def getHistoryData(request):
    param = []
    param.append(request.GET.get('fromDate'))
    param.append(request.GET.get('toDate'))
    param.append(int(request.GET.get('latestIndex')))
    param.append(int(request.GET.get('fromRow')))
    param.append(int(request.GET.get('rowLimitCount')))
    print(param)
    rsList = sqlCollection.get_history_data(param)

    return JsonResponse({'list': rsList[0], 'totalCount': rsList[1]})

def live(request):
    return render(request, 'templates/live.html')

def history(request):
    return render(request, 'templates/history.html')





def live_graph(request):
    return render(request, 'templates/live_graph.html')


def getLiveData_graph(request):
    rsList = sqlCollection.get_live_data()
    return JsonResponse(rsList)

def history_graph(request):
    return render(request, 'templates/history_graph.html')

def getHistoryData_graph(request):
    param = []
    param.append(request.GET.get('fromDate'))
    param.append(request.GET.get('toDate'))
    param.append(int(request.GET.get('latestIndex')))
    param.append(int(request.GET.get('fromRow')))
    param.append(int(request.GET.get('rowLimitCount')))
    print(param)
    rsList = sqlCollection.get_history_data(param)

    return JsonResponse({'list': rsList[0], 'totalCount': rsList[1]})
