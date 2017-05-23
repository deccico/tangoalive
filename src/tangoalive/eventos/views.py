# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.conf import settings
from django.utils import timezone

import random

from .models import Evento, Grupo, EventoEntrada


def get_last_eventos(page_from, quantity):
    results_from = page_from * quantity
    results_to = page_from * quantity + quantity
    eventos = Evento.objects.with_next_day()
    total = len(eventos)
    return total, eventos[results_from:results_to]

def get_last_highlighted(quantity):
    eventos = Evento.objects.with_next_day(with_highlight=True)
    return eventos[:quantity]

def get_eventos_from_grupo(grupo_name, quantity=10):
    return Evento.objects.filter(
        next_day__gte=timezone.now(),
        grupo__name=grupo_name
    ).order_by('next_day')[:quantity]

def get_grupos(page_from, quantity):
    results_from = page_from * quantity
    results_to = page_from * quantity + quantity
    grupos = Grupo.objects.filter(
        image_1__isnull=False
    ).exclude(image_1=u'').order_by('name')[results_from:results_to]
    total = len(Grupo.objects.filter(image_1__isnull=False).exclude(image_1=u''))
    return total, grupos

def home_page(request):
    _, latest_eventos_list = get_last_eventos(0, 6)
    latest_eventos_highlighted = get_last_highlighted(4)
    template = loader.get_template('eventos/index.html')
    print('len latest eventos {0}'.format(len(latest_eventos_list)))
    context = {
        'latest_eventos_list': latest_eventos_list,
        'latest_eventos_highlighted': latest_eventos_highlighted,
        'img_rnd_head': '{0:04d}'.format(random.randint(1, 27))
    }
    return HttpResponse(template.render(context, request))

def evento_detail(request, eventos_id):
    try:
        evento = Evento.objects.get(pk=eventos_id)
        select_pago='<select name="quantity"><option value="1">1 ticket</option>{0}</select>'
        additional_options = ''
        if evento.entradas_disponibles > 1:
            for i in range(2, evento.entradas_disponibles + 1):
                additional_options += '<option value={0}>{0} tickets</option>'.format(i)
            select_pago = select_pago.format(additional_options)
    except Evento.DoesNotExist:
        raise Http404("Código de evento inexistente.")
    return render(request, 'eventos/detail.html',
                  {'evento': evento,
                   'select_pago': select_pago,
                   'tipo_entradas': evento.tipo_entradas.all(),
                   'number_entradas': len(evento.tipo_entradas.all())
                   })

def evento_from_permalink(request, slug):
    try:
        evento = Evento.objects.get(permalink=slug)
    except:
        #couldn't find event. So so sorry...
        return HttpResponseRedirect("/eventos")
    return evento_detail(request, evento.id)

def browse_eventos(request):
    page_size = request.GET.get('q', '24')
    page_size = int(page_size) if page_size.isdigit() else 24
    page_from = request.GET.get('from', '0')
    page_from = int(page_from) if page_from.isdigit() else 0
    template = loader.get_template('eventos/browse_eventos.html')
    total, latest_eventos_list = get_last_eventos(page_from, page_size)
    context = {
        'latest_eventos_list': latest_eventos_list,
        'page_links': create_page_links(page_size, total, page_from, '/eventos')
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


def bandas(request):
    page_size = request.GET.get('q', '24')
    page_size = int(page_size) if page_size.isdigit() else 24
    page_from = request.GET.get('from', '0')
    page_from = int(page_from) if page_from.isdigit() else 0
    template = loader.get_template('eventos/browse_grupos.html')
    total, grupos = get_grupos(page_from, page_size)
    context = {
        'total': total,
        'grupos': grupos,
        'page_links': create_page_links(page_size, total, page_from, '/bandas')
    }
    return HttpResponse(template.render(context, request))


def banda_detail(request, grupo_id):
    try:
        grupo = Grupo.objects.get(pk=grupo_id)
        eventos = get_eventos_from_grupo(grupo.name, 10)
    except Evento.DoesNotExist:
        raise Http404("Grupo does not exist")
    return render(request, 'eventos/grupo_detail.html',
                  {'grupo': grupo,
                   'eventos': eventos,
                   })


def get_compra_obj(title, quantity, price, external_reference, picture_url):
    import mercadopago
    preference = {
        'external_reference': '{0}'.format(external_reference),
        "items": [
            {
                "title": title,
                "quantity": quantity,
                "currency_id": "ARS",
                "unit_price": price,
                "picture_url": picture_url,
            }
        ],
        'payment_methods': {
            'installments': 1,
            'excluded_payment_types': [
                {'id': 'ticket'},
                {'id': 'atm'},
            ],
        },
        u'back_urls': {
            'failure': '',
            'pending': 'http://tangoalive.com/eventos/payment_in_process',
            'success': 'http://tangoalive.com/eventos/payment_ok'
        },
    }
    mp = mercadopago.MP(settings.MP_CLIENT_ID, settings.MP_CLIENT_SECRET)
    preferenceResult = mp.create_preference(preference)
    url = preferenceResult["response"]["init_point"]
    return preferenceResult, url


def buy(request, eventos_id):
    #get event object based on the event id
    evento = get_object_or_404(Evento, pk=eventos_id)
    #get quantity from the form
    try:
        quantity = int(request.POST['quantity'])
        entrada_id = int(request.POST['entrada'])
    except:
        return HttpResponseRedirect("/")
    #create mp object with the right quantity and event id
    #forward to mp to let the user buy
    evento_entrada = get_object_or_404(EventoEntrada, pk=entrada_id)
    _, url = get_compra_obj("{0} - {1}".format(evento.name, str(evento_entrada.descripcion)), quantity, float(evento_entrada.precio), evento.id,
                          "http://tangoalive.com/media/{0}".format(evento.image_1))
    #redirect to MP site
    return HttpResponseRedirect(url)


def get_payment_amount(payment_id):
    import mercadopago
    mp = mercadopago.MP(settings.MP_CLIENT_ID, settings.MP_CLIENT_SECRET)
    payment = mp.get_payment(payment_id)
    amount = 0
    try:
        amount = float(payment["response"]["collection"]["transaction_amount"])
    except:
        amount = 0
    return amount


def payment_ok(request):
    #we land here because mp sent us...
    #todo: verify that mp actually sent this request
    #get event code from the mp variables
    event_id = request.GET.get('external_reference', '-1')
    event_id = int(event_id) if event_id.isdigit() else -1
    evento = get_object_or_404(Evento, pk=event_id)
    collection_id = request.GET.get('collection_id', '-1')
    collection_status = request.GET.get('collection_status', 'none')
    if collection_id == "-1" or collection_status != 'approved':
        return HttpResponseRedirect("/")
    #create mp object based on the event id
    #get the quantity from the mp object
    payment_amount = get_payment_amount(collection_id)
    #substract the quantity from the event
    quantity = int(round(payment_amount / float(evento.precio_entrada)))
    evento.entradas_disponibles = evento.entradas_disponibles - quantity
    evento.save()
    #send notifications
    #todo: send email to the buyer
    #todo: send email to ourselves
    #we need to redirect to avoid a refresh updating the db
    return HttpResponseRedirect("/eventos/payment_ok_render/{0}/{1}".format(evento.id, quantity))


def payment_ok_render(request, event_id, quantity):
    evento = get_object_or_404(Evento, pk=event_id)
    template = loader.get_template('eventos/payment_ok.html')
    context = {
        'evento':  evento,
        'message': 'Compraste {0} ticket/s para el evento: "{1}" '
                   'el {2} a las {3} en "{4}"'.format(int(quantity), evento,
                                                      evento.event_date.strftime("%d/%m"),
                                                      evento.time_from.strftime("%I:%M %p"),
                                                      evento.place),
    }
    return HttpResponse(template.render(context, request))


def payment_in_process(request):
    #show message that we will wait for payment confirmation
    # to send a ticket confirmation

    #make sure we have an actual payment
    event_id = request.GET.get('external_reference', '-1')
    event_id = int(event_id) if event_id.isdigit() else -1
    collection_id = request.GET.get('collection_id', '-1')
    #collection_status = request.GET.get('collection_status', 'none')
    if collection_id == "-1" or event_id == -1:
        return HttpResponseRedirect("/")
    #render page
    return render(request, 'eventos/payment_in_process.html', {})
