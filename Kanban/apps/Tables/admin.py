from django.contrib import admin
from .models import Projeto, Coluna, Item


admin.site.register(Projeto)
admin.site.register(Coluna)
admin.site.register(Item)