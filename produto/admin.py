from django.contrib import admin
from .models import Produto, Variacao

# Variação Inline
class VariacaoInline(admin.TabularInline):
    model = Variacao
    extra = 1

class ProdutoAdmin(admin.ModelAdmin):
    inlines = [
        VariacaoInline
    ]

admin.site.register(Produto, ProdutoAdmin)
admin.site.register(Variacao)
