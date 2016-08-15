from django.contrib import admin
from .models import Evento, EventoAdmin, Place, PlaceAdmin, EventoTipo, EventoTipoAdmin, Grupo, GrupoAdmin, Musico, MusicoAdmin, Portada

admin.site.register(Evento, EventoAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(EventoTipo, EventoTipoAdmin)
admin.site.register(Grupo, GrupoAdmin)
admin.site.register(Musico, MusicoAdmin)
admin.site.register(Portada)

