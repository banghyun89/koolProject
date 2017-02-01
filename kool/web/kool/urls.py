from django.conf.urls import url
from django.contrib import admin
from kool import views

urlpatterns = [
    url(r'^$', views.menu, name='home'),
    url(r'^live/$', views.live),
    url(r'^history/$', views.history),
    url(r'^live/getLiveData/$', views.getLiveData),
    url(r'^history/getHistoryData/$', views.getHistoryData),
    url(r'^admin/', admin.site.urls),
]
