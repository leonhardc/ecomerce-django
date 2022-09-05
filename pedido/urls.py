from django.urls import path
from . import views

app_name = 'pedido'

urlpatterns = [
    path('', views.Pagar.as_view(), nome='pagar'),
    path('fecharpedido/', views.FecharPedido.as_view(), nome='fecharpedido'),
    path('detalhe/', views.Detalhe.as_view(), nome='detalhe'),
]