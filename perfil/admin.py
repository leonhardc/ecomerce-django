from django.contrib import admin
from .models import Perfil

class PerfilAdmin(admin.ModelAdmin):
    list_display = [
        'usuario',
        'idade',
        'data_nascimento'
    ]

admin.site.register(Perfil, PerfilAdmin)

