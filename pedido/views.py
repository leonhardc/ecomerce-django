from ctypes import util
from django.shortcuts import render, redirect
from django.views.generic import ListView
from django.views import View
from django.contrib import messages
from produto.models import Variacao
from utils import utils
from .models import Pedido, ItemPedido

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


        carrinho = self.request.session.get('carrinho')
        carrinho_variacao_ids = [v for v in carrinho]
        # essa query usa .select_related('produto') onde:
        # .select_related('produto')
        # retorna um QuerySet que “seguirá” relacionamentos de chave estrangeira, selecionando 
        # impulsionador de desempenho que resulta em uma única consulta mais complexa, dados
        # adicionais de objetos relacionados ao executar sua consulta. Este é um mas significa que
        # o uso posterior de relacionamentos de chave estrangeira não exigirá consultas de banco de dados.
        bd_variacoes = list(
            Variacao.objects.select_related('produto').filter(id__in=carrinho_variacao_ids)
        )

        for variacao in bd_variacoes:
            error_msg_estoque = ""
            vid = str(variacao.id)

            estoque = variacao.estoque
            qtd_carrinho = carrinho[vid]['quantidade'] # quantidade de determinada variação no carrinho
            preco_unt = carrinho[vid]["preco_unitario"] # preco unitario
            preco_unt_promo = carrinho[vid]["preco_unitario_promocional"] # preco unitario promocional

            if estoque < qtd_carrinho:
                carrinho[vid]["quantidade"] = estoque
                carrinho[vid]["preco_quantitativo"] = estoque * preco_unt
                carrinho[vid]["preco_quantitativo_promocional"] = estoque * preco_unt_promo

                error_msg_estoque = "Estoque insificiente para alguns produtos do seu carrinho."

            if error_msg_estoque:  
                messages.error(
                    self.request,
                    
                )
                self.request.session.save()
                return redirect("produto:carrinho")

        qtd_total_carrinho = utils.cart_total_qtd(carrinho)
        valor_total_carrinho = utils.cart_totals(carrinho) 

        # Registrar pedido na base de dados
        pedido = Pedido(
            usuario = self.request.user,
            total = valor_total_carrinho,
            qtd_total = qtd_total_carrinho,
            status = "C",
        )

        pedido.save()

        ItemPedido.objects.bulk_create(
            [
                ItemPedido(
                    pedido=pedido,
                    produto=v['produto_nome'],
                    produto_id=v['produto_id'],
                    variacao=v['variacao_nome'],
                    variacao_id=v['variacao_id'],
                    preco=v['preco_quantitativo'],
                    preco_promocional=v['preco_quantitativo_promocional'],
                    quantidade=v['quantidade'],
                    imagem=v['imagem'],
                ) for v in carrinho.values()
            ]
        )
        del self.request.session['carrinho']
        return render(self.request, self.template_name)



class SalvarPedido(View):
    pass

class Detalhe(View):
    pass