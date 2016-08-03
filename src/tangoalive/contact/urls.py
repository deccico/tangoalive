from django.conf.urls import url
from . import views

app_name = "eventos"
urlpatterns = [
    url(r'^$', views.contact, name='contact'),
]
