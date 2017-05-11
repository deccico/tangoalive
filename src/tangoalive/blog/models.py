from __future__ import unicode_literals
import datetime

from django.contrib import admin
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

PICS_DIR = "%Y_%m/%d/%H_%M_%S/"


@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class TagAdmin(admin.ModelAdmin):
    ordering = ['name']

@python_2_unicode_compatible
class Blog(models.Model):
    BLOG_FOLDER_FORMAT = 'blog_pics/{0}/'.format(PICS_DIR)
    title = models.CharField(max_length=200)
    pub_date = models.DateField(default=datetime.datetime.now)
    foto = models.ImageField(upload_to=BLOG_FOLDER_FORMAT, blank=True, null=True)
    short_text = models.TextField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

class BlogAdmin(admin.ModelAdmin):
    ordering = ['title']
    show_full_result_count = True
    pub_date = models.DateField(default=datetime.datetime.now)
    tipo_evento = models.ForeignKey(Tag, blank=True, null=True)
    search_fields = ['title']
    save_on_top = True
    list_filter = ['pub_date']

