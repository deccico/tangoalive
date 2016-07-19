from django.http import HttpResponse
from django.http import Http404
from django.shortcuts import render
from django.template import loader

from .models import Evento


def index(request):
    latest_eventos_list = Evento.objects.order_by('-date')[:5]
    template = loader.get_template('eventos/index.html')
    context = {
        'latest_eventos_list': latest_eventos_list,
    }
    return HttpResponse(template.render(context, request))

def detail(request, eventos_id):
    try:
        evento = Evento.objects.get(pk=eventos_id)
    except Evento.DoesNotExist:
        raise Http404("Eventos does not exist")
    return render(request, 'eventos/detail.html', {'evento': evento})
