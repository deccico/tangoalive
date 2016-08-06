from django.http import HttpResponse
from django.template import loader

def browse(request):
    template = loader.get_template('search/browse.html')
    return HttpResponse(template.render({}, request))

