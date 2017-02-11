from django.conf.urls import url
from django.contrib import admin
from kool import views

urlpatterns = [
    url(r'^admin/', admin.site.urls),
    url(r'^$', views.menu, name='home'),
    url(r'^live/$', views.live, name='live'),
    url(r'^live/getLiveData/$', views.getLiveData),
    url(r'^live/getLiveData_chart/$', views.getLiveData_chart),
    url(r'^live_graph/$', views.live_graph, name='live_graph'),
    url(r'^live_graph/getLiveData/$', views.getLiveData_graph),
    url(r'^live_graph_01/$', views.live_graph_01, name='live_graph_01'),
    url(r'^live_graph_01/getLiveData/$', views.getLiveData_graph),
    url(r'^live_01/$', views.live_01, name='live_01'),
    url(r'^live_01/getLiveData/$', views.getLiveData),
    url(r'^history_graph/$', views.history_graph, name='history_graph'),
    url(r'^history_graph/getHistoryData/$', views.getHistoryData_graph),
    url(r'^history_01/$', views.history_01,name='history_01'),
    url(r'^history_01/getHistoryData/$', views.getHistoryData),
    url(r'^history/getHistoryData_list/$', views.getHistoryData_list),
    url(r'^history/$', views.history, name='history'),
    url(r'^history/getHistoryData/$', views.getHistoryData),

]
