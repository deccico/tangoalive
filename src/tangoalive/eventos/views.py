from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render
from django.template import loader
from django.utils import timezone

from .models import Evento, Portada, Grupo


def get_last_eventos(page_from, quantity):
    results_from = page_from * quantity
    results_to = page_from * quantity + quantity
    eventos = Evento.objects.filter(
        pub_date__lte=timezone.now(),
        event_date__gte=timezone.now(),
        image_1__isnull=False,
        description__gte=25
    ).exclude(image_1=u'').order_by('event_date')[results_from:results_to]
    #todo:cache this operation
    total = len(Evento.objects.filter(
                pub_date__lte=timezone.now(),
                event_date__gte=timezone.now(),
                image_1__isnull=False,
                description__gte=25
            ).exclude(image_1=u''))

    return total, eventos

def get_eventos_from_grupo(grupo_name, quantity=10):
    return Evento.objects.filter(
        pub_date__lte=timezone.now(),
        event_date__gte=timezone.now(),
        grupo__name=grupo_name
    ).order_by('event_date')[:quantity]

def get_grupos(page_from, quantity):
    results_from = page_from * quantity
    results_to = page_from * quantity + quantity
    grupos = Grupo.objects.filter(
        image_1__isnull=False
    ).exclude(image_1=u'').order_by('name')[results_from:results_to]
    #todo:cache this operation
    total = len(Grupo.objects.filter(image_1__isnull=False).exclude(image_1=u''))
    return total, grupos

def index(request):
    _, latest_eventos_list = get_last_eventos(0, 6)
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


def browse_eventos(request):
    page_size = request.GET.get('q', '24')
    page_size = int(page_size) if page_size.isdigit() else 24
    page_from = request.GET.get('from', '0')
    page_from = int(page_from) if page_from.isdigit() else 0
    template = loader.get_template('eventos/browse_eventos.html')
    total, latest_eventos_list = get_last_eventos(page_from, page_size)
    context = {
        'latest_eventos_list': latest_eventos_list,
        'page_links': create_page_links(page_size, total, page_from, '/browse_events')
    }
    return HttpResponse(template.render(context, request))


def create_page_links(page_size, total, page_index, link):
    items = ""
    count = 0
    while (count*page_size) < total:
        items += '<li class="{4}"><a href="{0}?from={1}&q={2}">{3}</a>' \
                 '</li>'.format(link, count, page_size, count+1, "active" if page_index==count else "")
        count += 1

    if page_index > 0:
        items = '<li><a href="{0}?from={1}&q={2}">Anterior</a></li>{3}'.format(link,
                                                                               page_index-1, page_size, items)
    if page_index < (count-1):
        items = '{3}<li><a href="{0}?from={1}&q={2}">Siguiente</a></li>'.format(link,
                                                                                page_index+1, page_size, items)
    page_links = '<nav><ul class="pagination-classic">{0}</ul></nav>'.format(items)
    return page_links


def browse_grupos(request):
    page_size = request.GET.get('q', '24')
    page_size = int(page_size) if page_size.isdigit() else 24
    page_from = request.GET.get('from', '0')
    page_from = int(page_from) if page_from.isdigit() else 0
    template = loader.get_template('eventos/browse_grupos.html')
    total, grupos = get_grupos(page_from, page_size)
    context = {
        'total': total,
        'grupos': grupos,
        'page_links': create_page_links(page_size, total, page_from, '/grupos/browse_grupos')
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

