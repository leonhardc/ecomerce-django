"""
    App produto

    Este app é o app que guarda as funcionalidades voltadas para manipulação de produtos
    no nosso e-comerce. Aqui é onde se detalha, se adiciona ao carrinho de compras etc.

    As funcionalidades desse app são listadas abaixo:

    1. Na url '', é a url principal da nossa aplicação, é nela que veremos todos os produtos
    presentes na nossa base de dados. Os produtos são listados em forma de carts simples, com foto
    nome e uma pequena descrição.

    2. Na url '<slug>', expomos os detalhes a cerca do produto escolhido na página principal,
    seu nome e sua descrição, se há variações e se o preço de cada variação.

    3. Na url 'adicionaraocarrinho/', é possivel adicionar o produto selecionado/detalhado ao carrinho
    de compras. para que possamos depois manipular nosso pedido.

    4. Na url 'removerdocarrinho/', é possivel removermos algum produto do nosso carrinho antes de termi-
    nármos o pedido.

    5. Na url 'carrinho/', é possível vermos como se encontra atualmente nosso carrinho de compras.

    6. Na url 'resumodacompra/', podemos finalmente ver o resumo da nossa compra, como preço final, já
    com adicionais de frete, descontos de cupom, dentre outros.

"""


from django.urls import path
from . import views

app_name = 'produto'

urlpatterns = [
    path('', views.ListaProdutos.as_view(), name='lista'),
    path('<slug>', views.DetalheProduto.as_view(), name='detalhe'),
    path('adicionaraocarrinho/', views.AdicionarAoCarrinho.as_view(), name='adicionaraocarrinho'),
    path('removerdocarrinho/', views.RemoverDoCarrinho.as_view(), name='removerdocarrinho'),
    path('carrinho/', views.Carrinho.as_view(), name='carrinho'),
    path('resumodacompra/', views.ResumoDaCompra.as_view(), name='resumodacompra'),
]