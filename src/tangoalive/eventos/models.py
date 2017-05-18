from __future__ import unicode_literals
import datetime
from django.contrib import admin
from django.db import models
from django.utils.encoding import python_2_unicode_compatible
from django.utils import timezone
from django.template.defaultfilters import slugify

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
    permalink = models.SlugField(max_length=50, unique=True, blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.permalink:
            self.permalink = slugify(self.permalink)
        else:
            self.permalink = self.permalink.lower()
        super(Grupo, self).save(*args, **kwargs)


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

    def get_dire(self):
        return "{0} {1} {2} {3}".format(
            "" if not self.address_line_1 else self.address_line_1,
            "" if not self.address_line_2 else self.address_line_2,
            "" if not self.address_city else self.address_city,
            "" if not self.address_province else self.address_province)

    def get_maps_url(self):
        maps_url = self.google_map_code
        if maps_url and len(maps_url) < 3:
            maps_url = maps_url.split('"')[0]
        else:
            maps_url = ""
        return maps_url


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
class EventoEntrada(models.Model):
    descripcion = models.CharField(max_length=50, default="General", blank=True, null=True)
    precio = models.DecimalField(default=0.0, decimal_places=2, max_digits=5)

    def __str__(self):
        return "{0} {1}".format(self.precio, self.descripcion)

class EventoEntradaAdmin(admin.ModelAdmin):
    ordering = ['precio']
    show_full_result_count = True
    save_on_top = True


class EventoManager(models.Manager):
    #reference: https://docs.djangoproject.com/en/1.11/topics/db/managers/#adding-extra-manager-methods
    def _next_day(self, keyword):
        yesterday = timezone.now() - datetime.timedelta(days = 1)
        #filter out incomplete events
        if not self.image_1 or len(self.description) < 25 or self.pub_date > timezone.now():
            return yesterday
        #filter out finished events
        if self.finish_date and self.finish_date < timezone.now():
            return yesterday
        #return next day if is in the future
        if self.event_date > timezone.now():
            return self.event_date
        #return next day if is in the past but the recurrence makes it active
        if self.weekly_recurrence:
            for i in range(7):
                computed_date = timezone.today() + datetime.timedelta(days = i)
                if computed_date.weekday() == self.weekly_recurrence:
                    return computed_date
        return yesterday

    def get(self, *args, **kwargs):
        print('ki--------------------------------------------------------------------')
        next_day = kwargs.pop('next_day', None)
        # Override #1) Query by dynamic property 'next_day'
        if next_day:
            ret = [('next_day',self._next_day())]
            kwargs = dict(kwargs.items() + ret.items())
        return super(EventoManager, self).get(*args, **kwargs)


@python_2_unicode_compatible
class Evento(models.Model):
    obj = EventoManager()

    EVENTOS_FOLDER_FORMAT = 'eventos_pics/{0}/'.format(PICS_DIR)
    name = models.CharField(max_length=200)
    grupo = models.ManyToManyField(Grupo, blank=True)
    tipo_evento = models.ForeignKey(EventoTipo, blank=True, null=True)
    description = models.TextField(blank=True, null=True)
    pub_date = models.DateField(default=datetime.datetime.now)
    event_date = models.DateField()
    time_from = models.TimeField()
    duration = models.DurationField()
    weekly_recurrence = models.SmallIntegerField(blank=True, null=True, choices=(
        (0,'monday'),
        (1,'tuesday'),
        (2,'wednesday'),
        (3,'thursday'),
        (4,'friday'),
        (5,'saturday'),
        (6,'sunday'),
    ))
    finish_date = models.DateField(blank=True, null=True)
    place = models.ForeignKey(Place, blank=True, null=True)
    highlighted = models.BooleanField(default=False)
    image_1 = models.ImageField(upload_to=EVENTOS_FOLDER_FORMAT, blank=True, null=True)
    image_2 = models.ImageField(upload_to=EVENTOS_FOLDER_FORMAT, blank=True, null=True)
    image_3 = models.ImageField(upload_to=EVENTOS_FOLDER_FORMAT, blank=True, null=True)
    image_4 = models.ImageField(upload_to=EVENTOS_FOLDER_FORMAT, blank=True, null=True)
    image_5 = models.ImageField(upload_to=EVENTOS_FOLDER_FORMAT, blank=True, null=True)
    entradas_disponibles = models.SmallIntegerField(default=0)
    tipo_entradas = models.ManyToManyField(EventoEntrada, blank=True)
    permalink = models.SlugField(blank=True, null=True, max_length=50)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.permalink:
            self.permalink = slugify(self.permalink)
        else:
            self.permalink = self.permalink.lower()
        super(Evento, self).save(*args, **kwargs)

    def get_precio(self):
        primera_entrada = self.tipo_entradas.all()
        if len(primera_entrada) == 0:
            return " no disponible"
        else:
            primera_entrada = primera_entrada[0]
        return "{0} &nbsp;{1}".format(primera_entrada.precio, primera_entrada.descripcion)

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


    #compute next date for a particular event. Return yesterday if none was found
    # def next_day(self):
    #     yesterday = timezone.now() - datetime.timedelta(days = 1)
    #     #filter out incomplete events
    #     if not self.image_1 or len(self.description) < 25 or self.pub_date > timezone.now():
    #         return yesterday
    #     #filter out finished events
    #     if self.finish_date and self.finish_date < timezone.now():
    #         return yesterday
    #     #return next day if is in the future
    #     if self.event_date > timezone.now():
    #         return self.event_date
    #     #return next day if is in the past but the recurrence makes it active
    #     if self.weekly_recurrence:
    #         for i in range(7):
    #             computed_date = timezone.today() + datetime.timedelta(days = i)
    #             if computed_date.weekday() == self.weekly_recurrence:
    #                 return computed_date
    #     return yesterday


class EventoAdmin(admin.ModelAdmin):
    filter_horizontal = ['grupo', 'tipo_entradas']
    list_display = ('id', 'name', 'place', 'pub_date', 'event_date',
                    'is_published', 'is_in_the_future', 'highlighted')
    list_filter = ['pub_date', 'event_date', 'highlighted']
    search_fields = ['name']
    ordering = ['event_date']
    show_full_result_count = True
    #radio_fields = {"place": admin.VERTICAL}
    #raw_id_fields = ('place',)
    save_on_top = True


