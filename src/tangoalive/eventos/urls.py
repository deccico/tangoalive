from django.conf.urls import url
from . import views

app_name = "eventos"
urlpatterns = [
    url(r'^$', views.browse_eventos, name='browse_eventos'),
    url(r'^(?P<eventos_id>[0-9]+)$', views.evento_detail, name='evento_detail'),
    url(r'^(?P<eventos_id>[0-9]+)/$', views.evento_detail, name='evento_detail'),
    url(r'^payment_ok$', views.payment_ok, name='payment_ok'),
    url(r'^payment_ok_render/(?P<event_id>[0-9]+)/(?P<quantity>[0-9]+)/$', views.payment_ok_render, name='payment_ok_render'),
    url(r'^payment_in_process$', views.payment_in_process, name='payment_in_process'),
    url(r'^(?P<eventos_id>[0-9]+)/buy/$', views.buy, name='buy'),
    url(r'^(?P<slug>[\w-]+)$', views.evento_from_permalink, name='evento_from_permalink'),
]
