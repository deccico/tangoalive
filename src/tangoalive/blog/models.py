from __future__ import unicode_literals
import datetime

from django.contrib import admin
from django.db import models
from django.template.defaultfilters import slugify
from django.utils.encoding import python_2_unicode_compatible

PICS_DIR = "%Y_%m/%d/%H_%M_%S/"


@python_2_unicode_compatible
class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class TagAdmin(admin.ModelAdmin):
    ordering = ['name']

@python_2_unicode_compatible
class Blog(models.Model):
    BLOG_FOLDER_FORMAT = 'blog_pics/{0}/'.format(PICS_DIR)
    title = models.CharField(max_length=200)
    pub_date = models.DateField(default=datetime.datetime.now)
    permalink = models.SlugField(max_length=50, unique=True)
    image_1 = models.ImageField(upload_to=BLOG_FOLDER_FORMAT, blank=True, null=True)
    image_2 = models.ImageField(upload_to=BLOG_FOLDER_FORMAT, blank=True, null=True)
    image_3 = models.ImageField(upload_to=BLOG_FOLDER_FORMAT, blank=True, null=True)
    short_text = models.TextField(blank=True, null=True)
    text = models.TextField(blank=True, null=True)
    tags = models.ManyToManyField(Tag, blank=True)

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        self.permalink = slugify(self.permalink)
        super(Blog, self).save(*args, **kwargs)

class BlogAdmin(admin.ModelAdmin):
    ordering = ['title']
    show_full_result_count = True
    pub_date = models.DateField(default=datetime.datetime.now)
    search_fields = ['title']
    save_on_top = True
    list_filter = ['pub_date']

