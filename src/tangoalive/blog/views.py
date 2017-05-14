# -*- coding: utf-8 -*-

from django.http import HttpResponse, HttpResponseRedirect, Http404
from django.shortcuts import render
from django.template import loader

from .models import Blog


def index(request):
    page_size = request.GET.get('q', '24')
    page_size = int(page_size) if page_size.isdigit() else 24
    page_from = request.GET.get('from', '0')
    page_from = int(page_from) if page_from.isdigit() else 0
    template = loader.get_template('blog/index.html')
    total, blogs = get_blogs(page_from, page_size)
    context = {
        'total': total,
        'blogs': blogs,
        'page_links': create_page_links(page_size, total, page_from, '/bandas')
    }
    return HttpResponse(template.render(context, request))


def blog_from_permalink(request, slug):
    try:
        blog = Blog.objects.get(permalink=slug)
    except:
        #couldn't find event. So so sorry...
        return HttpResponseRedirect("/blog")
    return blog_detail(request, blog.id)


def blog_detail(request, blog_id):
    try:
        blog = Blog.objects.get(pk=blog_id)
    except Blog.DoesNotExist:
        raise Http404("Código de blog inexistente.")
    return render(request, 'blog/detail.html',
                  {'blog': blog,
                   })


def get_blogs(page_from, quantity):
    results_from = page_from * quantity
    results_to = page_from * quantity + quantity
    blogs = Blog.objects.filter(
        image_1__isnull=False
    ).exclude(image_1=u'').order_by('title')[results_from:results_to]
    #todo:cache this operation
    total = len(Blog.objects.filter(image_1__isnull=False).exclude(image_1=u''))
    return total, blogs


#todo repeated form eventos page
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

