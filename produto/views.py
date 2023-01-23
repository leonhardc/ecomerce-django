from django.shortcuts import render, redirect, reverse, get_object_or_404
from django.views.generic.list import ListView
from django.views.generic.detail import DetailView
from django.views import View
from django.http import HttpResponse
from django.contrib import messages
from .models import Produto, Variacao
from perfil.models import Perfil
from comentarios.models import Comentario
import datetime


class ListaProdutos(ListView):
    """
        Lista todos os produtos da base de dados
    """
    model = Produto
    template_name = 'produto/lista.html'
    context_object_name = 'produtos'

# class DetalheProduto(DetailView):
#     """
#         Mostra os detalhes do produto selecionado na página principal
#     """

#     model = Produto
#     template_name = 'produto/detalhe.html'
#     context_object_name = 'produto'
#     slug_url_kwarg = 'slug'

class DetalheProduto(View):
    def get(self, *args, **kwargs):
        template_name = 'produto/detalhe.html'
        slug = kwargs['slug']

        produto = Produto.objects.filter(slug=slug).first()
        comentario_produto = Comentario.objects.filter(produto_comentario=produto).order_by('-data_comentario')

        contexto = {
            'produto': produto,
            'comentarios': comentario_produto
        }

        return render(
            self.request,
            template_name=template_name,
            context=contexto
        )

class AdicionarAoCarrinho(View):
    """
        Adiciona o produto selecionado no carrinho de compras
    """

    def get(self, *args, **kwargs):

        # HTTP_REFERER é um método que o django usa para guardar a referência da página
        # anteriormente acessada pelo usuário.
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')
        )

        # Em produto/templates/produto/detalhes.html a tag <select> implementa o atributo
        # name="vid", que nesse caso se refere ao Id da variação do produto.
        # O método abaixo - self.request.GET.get('vid') - implementa ima forma de capturarmos
        # o id da variação do produto para podermos, posteriormente, adicioná-lo ao carrinho de
        # compras.
        variacao_id = self.request.GET.get('vid')

        # se não existir uma variação do nosso produto retornamos para página acessada
        # anteriormente
        if not variacao_id:
            messages.error(
                self.request,
                'Produto não existe'
            )
            return redirect(http_referer)

        # Captura o objeto que representa a variação na nossa base de dados
        variacao = get_object_or_404(Variacao, id=variacao_id)
        variacao_estoque = variacao.estoque
        produto = variacao.produto

        produto_id = produto.id
        produto_nome = produto.nome
        variacao_nome = variacao.nome or ''
        preco_unitario = variacao.preco
        preco_unitario_promocional = variacao.preco_promocional
        quantidade = 1
        slug = produto.slug
        imagem = produto.imagem

        if imagem:
            imagem = imagem.name
        else:
            imagem = ''

        # Se o estoque for insuficiente, retornar uma mensagem de erro.
        if variacao.estoque < 1:
            messages.error(
                self.request,
                'Estoque insuficiente.'
            )
            return redirect(http_referer)

        # Se não existir um carrinho, criamos um carrinho.
        # Uma _.session funciona como os cookies no navegador, são informações do usuário
        # sobre dados da seção, mas que serão armazenadas pelo servidor, pelo tempo que for
        # necessário.
        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()

        # Acrescenta variação de produto ao carrinho
        carrinho = self.request.session['carrinho']
        if variacao_id in carrinho:
            quantidade_carrinho = carrinho[variacao_id]['quantidade']
            quantidade_carrinho += 1

            # Condição para determinar se a quantidade de produtos que o usuário quer
            # adicionar no carrinho é maior que a quantidade que existe em estoque na loja.
            if variacao_estoque < quantidade_carrinho:
                messages.error(
                    self.request,
                    f'Estoque insuficiente para {quantidade_carrinho}x no produto {produto_nome}.'
                    f'Adicionamos {variacao_estoque}x no seu carrinho.'
                )
                quantidade_carrinho = variacao_estoque

            # As proximas linhas fazem o cálculo do preço dos produtos que estão no carrinho.
            carrinho[variacao_id]['quantidade'] = quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo'] = preco_unitario * quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo_promocional'] = preco_unitario_promocional * \
                                                                      quantidade_carrinho


        else:
            carrinho[variacao_id] = {
                'produto_id':produto_id,
                'produto_nome':produto_nome,
                'variacao_nome':variacao_nome,
                'variacao_id':variacao_id,
                'preco_unitario':preco_unitario,
                'preco_unitario_promocional':preco_unitario_promocional,
                'preco_quantitativo':preco_unitario,
                'preco_quantitativo_promocional':preco_unitario_promocional,
                'quantidade': 1,
                'slug':slug,
                'imagem':imagem
            }

        # Salvando a sessão
        self.request.session.save()

        messages.success(
            self.request,
            f'Produto {produto_nome} adicionado ao seu carrinho '
            f'{carrinho[variacao_id]["quantidade"]}x.'
        )

        return redirect(http_referer)

class RemoverDoCarrinho(View):
    """
        Remove produto selecionado do carrinho de compras.
    """
    def get(self, *args, **kwargs):
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')
        )
        variacao_id = self.request.GET.get('vid')

        # Se o ID da variação do produto não existir
        if not variacao_id:
            return redirect(http_referer)

        # Se o carrinho não existir
        if not self.request.session.get('carrinho'):
            return redirect(http_referer)

        # ...
        if variacao_id not in self.request.session['carrinho']:
            return redirect(http_referer)

        # Produto removido do carrinho com sucesso.
        # Mensagem antes de realmente remover o produto, porque assim
        # é possível pegar o carrinho.
        carrinho = self.request.session['carrinho'][variacao_id]
        messages.success(
            self.request,
            f'Produto {carrinho["variacao_id"]} removido do Carrinho.'
        )

        # Removendo o produto do carrinho.
        del self.request.session['carrinho'][variacao_id]
        self.request.session.save()
        return redirect(http_referer)

class Carrinho(View):
    """
        Lista todos os produtos adicionados ao carrinho.
    """
    def get(self, *args, **kwargs):
        contexto = {
            'carrinho': self.request.session.get('carrinho', {})
        }
        return render(
            self.request,
            'produto/carrinho.html',
            contexto
        )

class Comprar(View):
    """
        Faz a compra de 1 produto somente
    """
    # TODO: Corrigit bug desta view. Não seleciona o produto para compra
    def get(self, *args, **kwargs):

        # HTTP_REFERER é um método que o django usa para guardar a referência da página
        # anteriormente acessada pelo usuário.
        http_referer = self.request.META.get(
            'HTTP_REFERER',
            reverse('produto:lista')
        )

        # Em produto/templates/produto/detalhes.html a tag <select> implementa o atributo
        # name="vid", que nesse caso se refere ao Id da variação do produto.
        # O método abaixo - self.request.GET.get('vid') - implementa ima forma de capturarmos
        # o id da variação do produto para podermos, posteriormente, adicioná-lo ao carrinho de
        # compras.
        print(self.request)
        variacao_id = self.request.GET.get('vid')

        # se não existir uma variação do nosso produto retornamos para página acessada
        # anteriormente
        if not variacao_id:
            messages.error(
                self.request,
                'Produto não existe'
            )
            return redirect(http_referer)

        # Captura o objeto que representa a variação na nossa base de dados
        variacao = get_object_or_404(Variacao, id=variacao_id)
        variacao_estoque = variacao.estoque
        produto = variacao.produto

        produto_id = produto.id
        produto_nome = produto.nome
        variacao_nome = variacao.nome or ''
        preco_unitario = variacao.preco
        preco_unitario_promocional = variacao.preco_promocional
        quantidade = 1
        slug = produto.slug
        imagem = produto.imagem

        if imagem:
            imagem = imagem.name
        else:
            imagem = ''

        # Se o estoque for insuficiente, retornar uma mensagem de erro.
        if variacao.estoque < 1:
            messages.error(
                self.request,
                'Estoque insuficiente.'
            )
            return redirect(http_referer)

        # Se não existir um carrinho, criamos um carrinho.
        # Uma _.session funciona como os cookies no navegador, são informações do usuário
        # sobre dados da seção, mas que serão armazenadas pelo servidor, pelo tempo que for
        # necessário.
        if not self.request.session.get('carrinho'):
            self.request.session['carrinho'] = {}
            self.request.session.save()

        # Acrescenta variação de produto ao carrinho
        carrinho = self.request.session['carrinho']
        if variacao_id in carrinho:
            quantidade_carrinho = carrinho[variacao_id]['quantidade']
            quantidade_carrinho += 1

            # Condição para determinar se a quantidade de produtos que o usuário quer
            # adicionar no carrinho é maior que a quantidade que existe em estoque na loja.
            if variacao_estoque < quantidade_carrinho:
                messages.error(
                    self.request,
                    f'Estoque insuficiente para {quantidade_carrinho}x no produto {produto_nome}.'
                    f'Adicionamos {variacao_estoque}x no seu carrinho.'
                )
                quantidade_carrinho = variacao_estoque

            # As proximas linhas fazem o cálculo do preço dos produtos que estão no carrinho.
            carrinho[variacao_id]['quantidade'] = quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo'] = preco_unitario * quantidade_carrinho
            carrinho[variacao_id]['preco_quantitativo_promocional'] = preco_unitario_promocional * \
                                                                      quantidade_carrinho


        else:
            carrinho[variacao_id] = {
                'produto_id':produto_id,
                'produto_nome':produto_nome,
                'variacao_nome':variacao_nome,
                'variacao_id':variacao_id,
                'preco_unitario':preco_unitario,
                'preco_unitario_promocional':preco_unitario_promocional,
                'preco_quantitativo':preco_unitario,
                'preco_quantitativo_promocional':preco_unitario_promocional,
                'quantidade': 1,
                'slug':slug,
                'imagem':imagem
            }

        # Salvando a sessão
        self.request.session.save()

        messages.success(
            self.request,
            f'Produto {produto_nome} adicionado ao seu carrinho '
            f'{carrinho[variacao_id]["quantidade"]}x.'
        )

        return redirect('produto:resumodacompra')

class ResumoDaCompra(View):

    template_name = 'produto/resumo.html'

    def get(self, *args, **kwargs):
        if not self.request.user.is_authenticated:
            return redirect('perfil:criar')

        perfil = Perfil.objects.filter(usuario=self.request.user).exists()
        
        # Finalizar compra somente se o usuário tiver perfil
        if not perfil: 
            messages.error(
                self.request, 
                "Usuário não tem perfil. Por favor termine seu cadastro antes de finalizar a compra."
                )
            return redirect('perfil:criar')

        # Finalizar compra somente se haver produtos no carrinho
        if not self.request.session.get('carrinho'):
            messages.error(
                self.request, 
                "Não há produtos no seu carrinho."
                )
            return redirect('produto:lista')            

        contexto = {
            'usuario': self.request.user,
            'carrinho': self.request.session['carrinho']
        }
        
        return render(self.request, self.template_name, context=contexto)


def adicionarComentario(request):
    """
        Esta view recebe o conteudo do formulário em produto/detalhe.html e guarda
        o comentário
    """
    if not request.user.is_authenticated:
        messages.error(request, "Antes de deixar sua avaliação faça login no nosso site.")
        return redirect(request.META.get('HTTP_REFERER'))

    if request.method == "POST":
        """
            Verficiar se o usuário está autenticado;
            Se sim, fazer comentário guardando:
                1. id do produto que será comentado
                2. id do usuario que comentou
                3. hora do comentario

            Se não, pedir para o usuário fazer login
        """
        referer = request.META.get('HTTP_REFERER')
        slug = referer.split('/')[-1]

        # Descobrir como resgatar o id fo produto que estou fazendo a busca
        produto = Produto.objects.get(slug = slug)
        comentario = request.POST.get('comentario')

        comentar = Comentario(
            comentario = comentario,
            produto_comentario = produto, 
            usuario_comentario = request.user
        )

        comentar.save()
        messages.success(request, "Comentário adicionado com sucesso!")
        return redirect(referer)

    messages.error(request, "Comentário não adicionado.")
    return redirect(request.META.get('HTTP_REFERER'))