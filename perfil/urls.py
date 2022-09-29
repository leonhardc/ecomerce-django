from django.urls import path
from . import views

app_name = 'perfil'

urlpatterns = [
    path('', views.Criar.as_view(), name='criar'),
    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),
    path('criarusuario/', views.CriarUsuario.as_view(), name='criar_usuario'),
    path('atualizar/', views.Atualizar.as_view(), name='atualizar'),
    path('deletarusuario/', views.DeletarUsuário.as_view(), name='deletar_usuario'),
    path('detalheperfil/', views.DetalhePerfil.as_view(), name='detalheperfil'),
    path('atualizarsenha/', views.AtualizarSenha.as_view(), name='atualizarsenha'),
]

