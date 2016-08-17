from __future__ import unicode_literals
import datetime
from django.contrib import admin
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone

PICS_DIR = "%Y_%m/%d/%H_%M_%S/"

@python_2_unicode_compatible
class Musico(models.Model):
    MUSICOS_FOLDER_FORMAT = 'musicos_pics/{0}/'.format(PICS_DIR)
    name = models.CharField(max_length=100)
    foto = models.ImageField(upload_to=MUSICOS_FOLDER_FORMAT, blank=True, null=True)
    biografia = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name


class MusicoAdmin(admin.ModelAdmin):
    ordering = ['name']
    show_full_result_count = True


@python_2_unicode_compatible\
#Grupo musical
class Grupo(models.Model):
    GRUPOS_FOLDER_FORMAT = 'grupos_pics/{0}/'.format(PICS_DIR)
    name = models.CharField(max_length=150)
    bio_corta = models.CharField(max_length=250, blank=True, null=True)
    bio_larga = models.TextField(blank=True, null=True)
    image_1 = models.ImageField(upload_to=GRUPOS_FOLDER_FORMAT, blank=True, null=True)
    image_2 = models.ImageField(upload_to=GRUPOS_FOLDER_FORMAT, blank=True, null=True)
    image_3 = models.ImageField(upload_to=GRUPOS_FOLDER_FORMAT, blank=True, null=True)
    image_4 = models.ImageField(upload_to=GRUPOS_FOLDER_FORMAT, blank=True, null=True)
    image_5 = models.ImageField(upload_to=GRUPOS_FOLDER_FORMAT, blank=True, null=True)
    musicos = models.ManyToManyField(Musico, blank=True)
    url = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    video_youtube = models.URLField(blank=True, null=True)
    soundcloud = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    spotify = models.URLField(blank=True, null=True)
    band_camp = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    embedded_video = models.CharField(max_length=800, blank=True, null=True)

    def __str__(self):
        return self.name

class GrupoAdmin(admin.ModelAdmin):
    filter_horizontal = ['musicos']
    ordering = ['name']
    show_full_result_count = True
    save_on_top = True

@python_2_unicode_compatible
class Place(models.Model):
    name = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    longitude = models.DecimalField(max_digits=10, decimal_places=7, blank=True, null=True)
    google_map_code = models.CharField(max_length=800, blank=True, null=True)
    address_line_1 = models.CharField(max_length=100)
    address_line_2 = models.CharField(max_length=100, blank=True, null=True)
    address_city = models.CharField(max_length=100, blank=True, null=True)
    address_province = models.CharField(max_length=100, blank=True, null=True)
    address_country = models.CharField(max_length=100, default='Argentina')
    telephone_1 = models.CharField(max_length=100, blank=True, null=True)
    telephone_2 = models.CharField(max_length=100, blank=True, null=True)
    telephone_3 = models.CharField(max_length=100, blank=True, null=True)
    owner = models.CharField(max_length=100, blank=True, null=True)
    transportation_options = models.TextField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)
    
    def __str__(self):
        return self.name

class PlaceAdmin(admin.ModelAdmin):
    ordering = ['name']
    show_full_result_count = True


@python_2_unicode_compatible
class EventoTipo(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class EventoTipoAdmin(admin.ModelAdmin):
    ordering = ['name']


@python_2_unicode_compatible  
class Evento(models.Model):
    EVENTOS_FOLDER_FORMAT = 'eventos_pics/{0}/'.format(PICS_DIR)
    name = models.CharField(max_length=200)
    grupo = models.ManyToManyField(Grupo, blank=True)
    tipo_evento = models.ForeignKey(EventoTipo, blank=True, null=True)
    precio = models.CharField(max_length=200, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    pub_date = models.DateField(default=datetime.datetime.now)
    event_date = models.DateField()
    time_from = models.TimeField()
    duration = models.DurationField()
    recurrent_definition = models.CharField(max_length=20, blank=True)
    place = models.ForeignKey(Place, blank=True, null=True)
    approved = models.BooleanField(default=False)
    image_1 = models.ImageField(upload_to=EVENTOS_FOLDER_FORMAT, blank=True, null=True)
    image_2 = models.ImageField(upload_to=EVENTOS_FOLDER_FORMAT, blank=True, null=True)
    image_3 = models.ImageField(upload_to=EVENTOS_FOLDER_FORMAT, blank=True, null=True)
    image_4 = models.ImageField(upload_to=EVENTOS_FOLDER_FORMAT, blank=True, null=True)
    image_5 = models.ImageField(upload_to=EVENTOS_FOLDER_FORMAT, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def is_published(self):
        return self.pub_date <= timezone.now().date()
    is_published.boolean = True
    is_published.admin_order_field = 'pub_date'
    is_published.short_description = 'Publicado?'

    def is_in_the_future(self):
        return self.event_date >= timezone.now().date()
    is_in_the_future.boolean = True
    is_in_the_future.admin_order_field = 'event_date'
    is_in_the_future.short_description = 'Activo?'


class EventoAdmin(admin.ModelAdmin):
    filter_horizontal = ['grupo']
    list_display = ('name', 'place', 'pub_date', 'event_date', 'is_published', 'is_in_the_future')
    list_filter = ['pub_date', 'event_date']
    search_fields = ['name']
    ordering = ['event_date']
    show_full_result_count = True
    #radio_fields = {"place": admin.VERTICAL}
    #raw_id_fields = ('place',)
    save_on_top = True

@python_2_unicode_compatible
class Portada(models.Model):
    PORTADA_FOLDER_FORMAT = 'portada_pics/'
    texto = models.TextField()
    image_1 = models.ImageField(upload_to=PORTADA_FOLDER_FORMAT, blank=True, null=True)
    image_2 = models.ImageField(upload_to=PORTADA_FOLDER_FORMAT, blank=True, null=True)
    image_3 = models.ImageField(upload_to=PORTADA_FOLDER_FORMAT, blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return "Portada"

