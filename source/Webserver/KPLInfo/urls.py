from django.conf.urls import url
from .import views

app_name='KPLInfo'
urlpatterns = [
    url(r'^$', views.menu, name='home'),
    url(r'^live$', views.live),
    url(r'^history$', views.history),
]