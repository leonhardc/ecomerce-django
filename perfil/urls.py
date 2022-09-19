"""
    App perfil

        Este app trata inicialmente de funcionalidades básicas relacionadas ao perfil de um
    usuário, coisas como nome completo, idade, endereço, para se saber como será enviado
    o pedido para esse usuário.

        As funcionalidades iniciais deste app são as seguintes:

    1. Na url '', é possível criar um perfil de usuário e se obter informações mais
    concretas sobre o usuário do sistema, como nome, idade, cep, data de nascimento.

    2. Na url 'atualizar', é possível atualizar algumas informações que a princípio,
    podem ter sido cadastradas errado ou informações que podem mudar com o tempo
    (ex. Endereço, cep, rua etc).

    3. Nas urls 'login/' e 'logout/' são url funcionais, que fazem ou desfazem o login
    do usuário no sistema, para que este possa concretizar o processo de compra dos pro-
    dutos.

"""

from django.urls import path
from . import views


app_name = 'perfil'

urlpatterns = [
    path('', views.Criar.as_view(), name='criar'),
    path('atualizar/', views.Atualizar.as_view(), name='atualizar'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
]