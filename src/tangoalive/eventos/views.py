from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render
from django.template import loader
from django.utils import timezone

from .models import Evento, Portada


def index(request):
    latest_eventos_list = get_last_eventos()
    template = loader.get_template('eventos/index.html')
    portada = Portada.objects.get(id=1)
    context = {
        'latest_eventos_list': latest_eventos_list,
        'portada': portada
    }
    return HttpResponse(template.render(context, request))

def detail(request, eventos_id):
    try:
        evento = Evento.objects.get(pk=eventos_id)
    except Evento.DoesNotExist:
        raise Http404("Eventos does not exist")
    return render(request, 'eventos/detail.html', {'evento': evento})

def get_last_eventos(quantity=3):
    """
    Return the last quantity published eventos (not including those set to be
    published in the future).
    """
    return Evento.objects.filter(
        pub_date__lte=timezone.now()).exclude(image_1=u'').order_by('-pub_date')[:quantity]


def browse(request):
    template = loader.get_template('eventos/browse.html')
    return HttpResponse(template.render({}, request))
