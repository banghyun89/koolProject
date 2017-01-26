from django.shortcuts import render
from django.http import HttpResponse
# Create your views here.

def menu(request):
    return render(request, 'KPLInfo/menu.html')

def live(request):
    return render(request, 'KPLInfo/live.html')


def history(request):
    return render(request, 'KPLInfo/history.html')

#def requestHistoryData(request):


#def requestLiveData(request):