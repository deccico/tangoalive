# -*- coding: utf-8 -*-

from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.http import Http404
from django.shortcuts import render, get_object_or_404
from django.template import loader
from django.utils.html import escape
from django.utils import timezone

from .models import Evento, Portada, Grupo

import datetime

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
                  {'evento': evento, 'select_pago': select_pago})


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
                   'eventos': eventos,
                   })


def buy(request, eventos_id):
    evento = get_object_or_404(Evento, pk=eventos_id)
    try:
        quantity = int(request.POST['quantity'])
    except:
        return HttpResponseRedirect("/")

    return render(request, 'eventos/payment_ok.html', {
        'message': 'Compraste {0} tickets, para el evento "{1}" '
                   'el {2} a las {3} en "{4}"'.format(quantity, evento,
                                                      evento.event_date.strftime("%d/%m"),
                                                      evento.time_from.strftime("%I:%M %p"),
                                                      evento.place),
    })

    pass
    #get quantity from the form (quantity element from the form)
    #get event id from the form (event_id from the form)
    #get event object based on the event id
    #create mp object with the right quantity and event id
    #forward to mp to let the user buy

    #evento = get_object_or_404(Evento, pk=eventos_id)


    #
    # evento.votes += 1
    # selected_choice.save()
    # # Always return an HttpResponseRedirect after successfully dealing
    # # with POST data. This prevents data from being posted twice if a
    # # user hits the Back button.
    # return HttpResponseRedirect(reverse('polls:results', args=(question.id,)))

    # import os, sys
    # import mercadopago
    # import json
    #
    # def index(req, **kwargs):
    # 	preference = {
    # 		"items": [
    # 			{
    # 				"title": "Multicolor kite",
    # 				"quantity": 1,
    # 				"currency_id": "ARS", # Available currencies at: https://api.mercadopago.com/currencies
    # 				"unit_price": 10.0
    # 			}
    # 		]
    # 	}
    # 	mp = mercadopago.MP("4971587513296525", "yugVAP2luDGtCX32vQzw9KoZ2Q0FnC21")
    #
    # 	preferenceResult = mp.create_preference(preference)
    #
    # 	url = preferenceResult["response"]["init_point"]
    #
    # 	output = """
    # 	<!doctype html>
    # 	<html>
    # 		<head>
    # 			<title>Pay</title>
    # 		</head>
    # 		<body>
    # 			<a href="{url}">Pay</a>
    # 		</body>
    # 	</html>
    # 	""".format (url=url)
    #
    # 	return output

def payment_ok(request):
    #we land here because mp sent us...
    #get event code from the mp variables
    #create mp object based on the event id
    #get the quantity from the mp object
    #get the buyer email from the mp object
    #substract the quantity from the event
    #send email to the buyer
    #send email to ourselves
    return render(request, 'eventos/payment_ok.html', {})

    # #make sure we have an actual payment
    # event_id = request.GET.get('external_reference', '-1')
    # event_id = int(event_id) if event_id.isdigit() else -1
    # collection_id = request.GET.get('collection_id', '-1')
    # collection_status = request.GET.get('collection_status', 'none')
    # print collection_id, collection_status, event_id
    # if collection_id == "-1" or collection_status <> 'approved' or event_id == -1:
    #     return HttpResponseRedirect("/")
    # evento = None
    # try:
    #     evento = Evento.objects.get(pk=event_id)
    # except Evento.DoesNotExist:
    #     #todo: add banner with error
    #     return HttpResponseRedirect("/")
    # if evento:
    #     #update tickets available
    #     evento.entradas_disponibles = evento.entradas_disponibles - 1
    #     evento.save()
    # #render page
    # return render(request, 'eventos/payment_ok.html', {})

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
