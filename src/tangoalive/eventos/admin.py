from django.contrib import admin
from .models import Evento, EventoAdmin, Place, EventoTipo, Grupo, GrupoAdmin, Musico, Portada

admin.site.register(Evento, EventoAdmin)
admin.site.register(Place)
admin.site.register(EventoTipo)
admin.site.register(Grupo, GrupoAdmin)
admin.site.register(Musico)
admin.site.register(Portada)

