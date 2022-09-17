from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views import View
from django.contrib import messages


class Pagar(View):
    template_name = 'pedido/pagar.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            messages.error(
                self.request,
                'Você precisa fazer login'
            )
            redirect('perfil:criar')

        if not self.request.session.get('carrinho'):
            messages.error(
                self.request,
                'carrinho vazio'
            )
            redirect('produto:lista')


        contexto = {}
        return render(self.request, self.template_name, contexto)


class SalvarPedido(View):
    pass

class Detalhe(View):
    pass