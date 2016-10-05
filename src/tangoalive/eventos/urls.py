from django.conf.urls import url
from . import views

app_name = "eventos"
urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /eventos/5/
    url(r'^(?P<eventos_id>[0-9]+)/$', views.detail, name='detail'),
    url(r'^browse_grupos$', views.browse_grupos, name='browse_grupos'),
    url(r'^grupo/(?P<grupo_id>[0-9]+)/$', views.grupo_detail, name='grupo_detail'),
    url(r'^payment_ok$', views.payment_ok, name='payment_ok'),
    url(r'^payment_in_process$', views.payment_in_process, name='payment_in_process'),
    url(r'^(?P<eventos_id>[0-9]+)/buy/$', views.buy, name='buy'),
]
