from django.conf.urls import url
from django.contrib import admin
from kool import views

urlpatterns = [
    url(r'^$', views.menu, name='home'),
    url(r'^live/$', views.live, name='live'),
    url(r'^history/$', views.history,name='history'),
    url(r'^live/getLiveData/$', views.getLiveData),
    url(r'^history/getHistoryData/$', views.getHistoryData),
    url(r'^admin/', admin.site.urls),
    url(r'^live_graph/$', views.live_graph, name='live_graph'),
    url(r'^live_graph/getLiveData/$', views.getLiveData_graph),
    url(r'^history_graph/$', views.history_graph, name='history_graph'),
    url(r'^history_graph/getHistoryData/$', views.getHistoryData_graph),
]
