from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    # ex: /eventos/5/
    url(r'^(?P<eventos_id>[0-9]+)/$', views.detail, name='detail'),
]
