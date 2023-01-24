from django.urls import path
from . import views

app_name = 'perfil'

urlpatterns = [
    path('', views.DetalhePerfil.as_view(), name='detalheperfil'),

    path('login/', views.Login.as_view(), name='login'),
    path('logout/', views.Logout.as_view(), name='logout'),

    path('criarusuario/', views.CriarUsuario.as_view(), name='criar'),
    path('atualizar/', views.Atualizar.as_view(), name='atualizar'),
    path('deletarusuario/', views.DeletarUsuário.as_view(), name='deletar_usuario'),
    
    path('updateuserinfo/', views.updateUserInfo , name="update_user_info"),
    path('updateuseradress/', views.updateUserAdress, name="update_user_adress"),
    path('updatePassword/', views.updatePassword, name="update_password"),
    path('atualizarsenha/', views.AtualizarSenha.as_view(), name='atualizarsenha'),
]

