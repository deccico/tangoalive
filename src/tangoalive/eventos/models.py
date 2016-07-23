from __future__ import unicode_literals
import datetime
from django.db import models
from django.utils.encoding import python_2_unicode_compatible

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

@python_2_unicode_compatible
class Grupo(models.Model):
    GRUPOS_FOLDER_FORMAT = 'grupos_pics/{0}/'.format(PICS_DIR)
    name = models.CharField(max_length=150)
    description = models.TextField(blank=True, null=True)
    image_1 = models.ImageField(upload_to=GRUPOS_FOLDER_FORMAT, blank=True, null=True)
    image_2 = models.ImageField(upload_to=GRUPOS_FOLDER_FORMAT, blank=True, null=True)
    image_3 = models.ImageField(upload_to=GRUPOS_FOLDER_FORMAT, blank=True, null=True)
    image_4 = models.ImageField(upload_to=GRUPOS_FOLDER_FORMAT, blank=True, null=True)
    image_5 = models.ImageField(upload_to=GRUPOS_FOLDER_FORMAT, blank=True, null=True)
    musicos = models.ManyToManyField(Musico, blank=True)
    url = models.URLField(blank=True, null=True)
    video_youtube = models.URLField(blank=True, null=True)
    soundcloud = models.URLField(blank=True, null=True)
    spotify = models.URLField(blank=True, null=True)
    twitter = models.URLField(blank=True, null=True)
    facebook = models.URLField(blank=True, null=True)
    band_camp = models.URLField(blank=True, null=True)
    notes = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.name

@python_2_unicode_compatible
class Place(models.Model):
    name = models.CharField(max_length=200)
    latitude = models.DecimalField(max_digits=10, decimal_places=7)
    longitude = models.DecimalField(max_digits=10, decimal_places=7)
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

@python_2_unicode_compatible
class EventoTipo(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

@python_2_unicode_compatible  
class Evento(models.Model):
    EVENTOS_FOLDER_FORMAT = 'eventos_pics/{0}/'.format(PICS_DIR)
    name = models.CharField(max_length=200)
    grupo = models.ForeignKey(Grupo, blank=True, null=True)
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

