from django.contrib import admin
from .models import Brigada, Batallones, Armas, Municiones, Personas, BrigadaDigital, UnidadDigital
# Register your models here.

admin.site.register(Brigada)
admin.site.register(Batallones)
admin.site.register(Armas)
admin.site.register(Municiones)
admin.site.register(Personas)
