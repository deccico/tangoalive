import random

from django.http import HttpResponse
from django.template import loader

def about(request):
    template = loader.get_template('contact/about.html')
    context = {
        'img_rnd': '{0:04d}'.format(random.randint(1, 16)),
    }
    return HttpResponse(template.render(context, request))
