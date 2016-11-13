from django.contrib import admin
from .models import Evento, EventoAdmin, Place, PlaceAdmin, EventoTipo, EventoTipoAdmin
from .models import Grupo, GrupoAdmin, Musico, MusicoAdmin
from .models import EventoEntrada, EventoEntradaAdmin

admin.site.register(Evento, EventoAdmin)
admin.site.register(EventoTipo, EventoTipoAdmin)
admin.site.register(Place, PlaceAdmin)
admin.site.register(EventoEntrada, EventoEntradaAdmin)
admin.site.register(Grupo, GrupoAdmin)
admin.site.register(Musico, MusicoAdmin)

