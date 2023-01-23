from django.contrib import admin
from .models import Comentario

class ComentarioAdmin(admin.ModelAdmin):
    list_display = [
        'produto_comentario',
        'produto_comentario',
        'usuario_comentario',
        'data_comentario',
        'publicado_comentario',
    ]

admin.site.register(Comentario, ComentarioAdmin)


