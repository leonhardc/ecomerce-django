from django.shortcuts import render
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from .models import Produto


class ListaProdutos(ListView):
    model = Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'

class DetalheProduto(DetailView):
    model = Produto
    template_name = 'produto/detalhe.html'
    context_object_name = 'produto'
    slug_url_kwarg = 'slug'

class AdicionarAoCarrinho(View):
    pass

class RemoverDoCarrinho(View):
    pass

class Carrinho(View):
    pass

class Finalizar(View):
    pass
