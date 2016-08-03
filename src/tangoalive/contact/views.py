from django.http import HttpResponse
from django.template import loader

def contact(request):
    template = loader.get_template('contact/contact.html')
    return HttpResponse(template.render({}, request))

def about(request):
    template = loader.get_template('contact/about.html')
    return HttpResponse(template.render({}, request))
