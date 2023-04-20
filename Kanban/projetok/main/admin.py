from django.contrib import admin
from .models import Perfil

class PerfilAdmin(admin.ModelAdmin):
    list_display = ('user', 'nome', 'idade', 'genero', 'descricao', 'foto_perfil', 'foto_banner')

admin.site.register(Perfil, PerfilAdmin)
