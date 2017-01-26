from django.conf.urls import url
from .import views

app_name='KPLInfo'
urlpatterns = [
    url(r'^$', views.menu, name='home'),   #위의 urls.py와는 달리 inlcude가 없습니다.
    # $를 붙이는 경우는 빈경로의 의미
    url(r'^live/$', views.live),
    url(r'^history/$', views.history),
    # url(r'^polls/(?P<poll_id>\d+)/$',views.polls),
    # url(r'^candidates/(?P<name>[가-힣]+)/$', views.candidates)
]