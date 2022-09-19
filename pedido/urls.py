"""
    App pedido.

        Neste app se concentra em características básicas de um pedido em
    um processo de compra, como por exemplo, pagar o pedido, salvar o
    pedido para pagar depois e claro, detalhar o pedido, para o cliente
    poder revisar e ter a certeza que os produtos no carrinho são mesmo
    o que ele quer.

        Este app tem inicialmente, as três funcionalidades descritas logo acima:

    1. Na url '', é possível escolher o método de pagamento do que está no carrinho.
    2. Na url 'salvarpedido/', é possível salvar o pedido na base de dados sem perder
    o que está no carrinho.
    3. Na url 'detalhe/', é possível detalhar o que é cada produto/variação e se ter
    noção, mesmo que de maneira redundante, do que se pediu.
    
"""


from django.urls import path
from . import views

app_name = 'pedido'

urlpatterns = [
    path('', views.Pagar.as_view(), name='pagar'),
    path('salvarpedido/', views.SalvarPedido.as_view(), name='salvarpedido'),
    path('detalhe/', views.Detalhe.as_view(), name='detalhe'),
]