from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render
from django.template import loader
from django.utils import timezone

from .models import Evento, Portada, Grupo


def get_last_eventos(quantity=3):
    """
    Return the last quantity published eventos (not including those set to be
    published in the future).
    """
    return Evento.objects.filter(
        pub_date__lte=timezone.now(),
        event_date__gte=timezone.now(),
        image_1__isnull=False,
        description__gte=25
    ).exclude(image_1=u'').order_by('event_date')[:quantity]

def get_eventos_from_grupo(grupo_name, quantity=10):
    return Evento.objects.filter(
        pub_date__lte=timezone.now(),
        event_date__gte=timezone.now(),
        grupo__name=grupo_name
    ).order_by('event_date')[:quantity]


def get_bandas(quantity=3):
    return Grupo.objects.filter(
        image_1__isnull=False
    ).exclude(image_1=u'').order_by('name')[:quantity]


def index(request):
    latest_eventos_list = get_last_eventos(6)
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

def browse(request):
    latest_eventos_list = get_last_eventos(50)
    template = loader.get_template('eventos/browse_eventos.html')
    portada = Portada.objects.get(id=1)
    context = {
        'latest_eventos_list': latest_eventos_list,
        'portada': portada
    }
    return HttpResponse(template.render(context, request))

def browse_grupos(request):
    grupos = get_bandas(50)
    template = loader.get_template('eventos/browse_grupos.html')
    context = {
        'grupos': grupos
    }
    return HttpResponse(template.render(context, request))

def grupo_detail(request, grupo_id):
    try:
        grupo = Grupo.objects.get(pk=grupo_id)
        eventos = get_eventos_from_grupo(grupo.name, 10)
    except Evento.DoesNotExist:
        raise Http404("Grupo does not exist")
    return render(request, 'eventos/grupo_detail.html',
                  {'grupo': grupo,
                   'eventos': eventos
                   })
