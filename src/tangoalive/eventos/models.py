from __future__ import unicode_literals
from operator import itemgetter
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
    def with_next_day(self, with_highlight=False, id=None, grupo_name=None, slug=None):
        if id:
            eventos = Evento.objects.get(pk=id)
        elif slug:
            eventos = Evento.objects.get(permalink=slug)
        else:
            eventos = Evento.objects.filter(pub_date__lte=timezone.now())
            if with_highlight:
                eventos = eventos.filter(highlighted=True)
            if grupo_name:
                eventos = eventos.filter(grupo__name=grupo_name)

        if not eventos:
            raise RuntimeError("Couldn't find any evento object with data with highlight:{0} id:{1} grupo_name:{2} "
                               "slug:{3}".format(with_highlight, id, grupo_name, slug))

        is_single_object = False
        print eventos.__class__.__name__
        if eventos.__class__.__name__ == "Evento":
            is_single_object = True
            eventos = [eventos]

        eventos_next_day = []
        #idea: modify queryset. Maybe based on: http://stackoverflow.com/questions/18255290/how-to-create-an-empty-queryset-and-to-add-objects-manually-in-django#18255443
        for e in eventos:
            print("loopisEvento")
            evento = {'id':e.id,
                      'image_1': e.image_1,
                      'image_2': e.image_2,
                      'image_3': e.image_3,
                      'image_4': e.image_4,
                      'image_5': e.image_5,
                      'name': e.name,
                      'place': e.place,
                      'get_precio': e.get_precio,
                      'tipo_evento': e.tipo_evento,
                      'description': e.description,
                      'time_from': e.time_from,
                      'duration': e.duration,
                      'entradas_disponibles': e.entradas_disponibles,
                      'tipo_entradas': e.tipo_entradas,
                      'permalink': e.permalink,
                      'notes': e.notes,
                      }
            if e.finish_date and e.finish_date < timezone.now().date():
                continue
            elif e.event_date >= timezone.now().date():
                evento['next_day'] = e.event_date
                eventos_next_day.append(evento)
            elif e.weekly_recurrence:
                for i in range(7):
                    computed_date = timezone.now().date() + datetime.timedelta(days = i)
                    if computed_date.weekday() == e.weekly_recurrence:
                        evento['next_day'] = computed_date
                        eventos_next_day.append(evento)

        if is_single_object:
            #we have only one object and we expect only one object
            return eventos_next_day[0] if len(eventos_next_day) else eventos[0]

        eventos = sorted(eventos_next_day, key=itemgetter('next_day'), reverse=False)
        return eventos


@python_2_unicode_compatible
class Evento(models.Model):
    objects = EventoManager()

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
        if self.event_date >= timezone.now().date():
            return True
        else:
            if self.finish_date and self.finish_date > timezone.now().date() and self.weekly_recurrence:
                return True
            if not self.finish_date and self.weekly_recurrence:
                return True
        return False

    is_in_the_future.boolean = True
    is_in_the_future.admin_order_field = 'event_date'
    is_in_the_future.short_description = 'Activo?'



class EventoAdmin(admin.ModelAdmin):
    filter_horizontal = ['grupo', 'tipo_entradas']
    list_display = ('id', 'name', 'permalink', 'place', 'pub_date', 'event_date',
                    'is_published', 'weekly_recurrence', 'finish_date',
                    'is_in_the_future', 'highlighted')
    list_filter = ['pub_date', 'event_date', 'highlighted']
    search_fields = ['name']
    ordering = ['event_date']
    show_full_result_count = True
    #radio_fields = {"place": admin.VERTICAL}
    #raw_id_fields = ('place',)
    save_on_top = True


