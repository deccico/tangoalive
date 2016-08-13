from django.contrib import admin
from .models import Evento, EventoAdmin, Place, EventoTipo, Grupo, Musico, Portada

admin.site.register(Evento, EventoAdmin)
admin.site.register(Place)
admin.site.register(EventoTipo)
admin.site.register(Grupo)
admin.site.register(Musico)
admin.site.register(Portada)

