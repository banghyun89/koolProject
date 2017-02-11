import sys
sys.path.append("..")
from django.shortcuts import render
from django.http import JsonResponse
from dbConn import sqlCollection
from datetime import datetime, timedelta

def menu(request):
    return render(request, 'templates/menu.html')


def live(request):
    return render(request, 'templates/live.html')

def live_01(request):
    return render(request, 'templates/live_01.html')

def live_graph(request):
    return render(request, 'templates/live_graph.html')

def live_graph_01(request):
    return render(request, 'templates/live_graph_01.html')

def history(request):
    return render(request, 'templates/history.html')

def history_01(request):
    return render(request, 'templates/history_01.html')

def history_graph(request):
    return render(request, 'templates/history_graph.html')


def getLiveData(request):
    rsList = sqlCollection.get_live_data()
    return JsonResponse(rsList)

def getLiveData_chart(request):
    rsList = sqlCollection.get_live_data_chart(request.GET.get('sensor'))
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

def getLiveData_graph(request):
    rsList = sqlCollection.get_live_data()
    return JsonResponse(rsList)


def getHistoryData_graph(request):
    param = []
    param.append(request.GET.get('fromDate'))
    param.append(request.GET.get('toDate'))
    param.append(int(request.GET.get('latestIndex')))
    param.append(int(request.GET.get('fromRow')))
    param.append(int(request.GET.get('rowLimitCount')))
    print(param)
    rsList = sqlCollection.get_history_data(param)

    return JsonResponse({'list': rsList[0], 'totalCount': rsList[1], 'maxId':rsList[2]})

def getHistoryData_list(request):
    param = []
    param.append(request.GET.get('fromDate'))
    param.append(request.GET.get('toDate'))
    param.append(request.GET.get('period'))

    list = request.GET.get('list')
    if list != "" :
       list = list.split(",")
    else :
        list = []
    param.append(list)
    print(param)

    rsList = sqlCollection.get_history_data_list(param)

    return JsonResponse({'selectColList': rsList[0], 'list': rsList[1], 'totalCount': rsList[2]})
