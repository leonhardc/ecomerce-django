from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.models import User
from django.contrib import auth
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.views import View
from django.views.generic.list import ListView
from . import models, forms
import copy
from django.http import HttpResponse


class BasePerfil(View):
    # template_name = 'perfil/criar.html'
    template_name = 'perfil/login-signup.html'

    def setup(self, *args, **kwargs):
        super().setup(*args, **kwargs)

        self.carrinho = copy.deepcopy(self.request.session.get('carrinho', {}))
        self.perfil = None

        if self.request.user.is_authenticated: # se usuário está autenticado

            self.perfil = models.Perfil.objects.filter(
                usuario=self.request.user
            ).first()

            self.contexto = {
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                    usuario=self.request.user,
                    instance=self.request.user
                ),
                'perfilform': forms.PerfilForm(
                    data=self.request.POST or None,
                    instance = self.perfil
                )
            }
        else:
            self.contexto = {
                'userform': forms.UserForm(data=self.request.POST or None),
                'perfilform': forms.PerfilForm(data=self.request.POST or None)
            }

        self.userform = self.contexto['userform']
        self.perfilform = self.contexto['perfilform']

        if self.request.user.is_authenticated:
            self.template_name = 'perfil/atualizar.html '

        self.renderizar = render(
            self.request,
            self.template_name,
            self.contexto
        )

    def get(self, *args, **kwargs):
        return self.renderizar

class Criar(BasePerfil):
    def post(self, *args, **kwargs):
        # Se um dos dois formuçários é inválido
        if not self.userform.is_valid() or not self.perfilform.is_valid():
            return self.renderizar

        username = self.userform.cleaned_data.get('username')
        password = self.userform.cleaned_data.get('password')
        email = self.userform.cleaned_data.get('email')
        first_name = self.userform.cleaned_data.get('first_name')
        last_name = self.userform.cleaned_data.get('last_name')


        # Usuário Logado | Atualizar
        if self.request.user.is_authenticated:
            usuario = get_object_or_404(
                User,
                username=self.request.user.username
            )
            usuario.username = username

            if password:
                usuario.set_password(password)

            usuario.email = email
            usuario.first_name = first_name
            usuario.last_name = last_name

            if not self.perfil:
                perfil = models.Perfil(**self.perfilform.cleaned_data)
                perfil.save()

            else:
                perfil = self.perfilform.save(commit=False)
                perfil.usuario = usuario
                perfil.save()
        # Usuário não logado (Novo usuário)
        else:
            # não salvar o usuário ainda na base de dados
            usuario = self.userform.save(commit=False)
            usuario.set_password(password)
            usuario.save()

            perfil = self.perfilform.save(commit=False)
            perfil.usuario = usuario
            perfil.save()

        if password:
            autentica = authenticate(
                self.request,
                username=usuario,
                password=password
            )

            if autentica:
                login(
                    self.request,
                    user=usuario
                )

        self.request.session['carrinho'] = self.carrinho
        self.request.session.save()

        messages.success(
            self.request,
            'Seu cadastro foi criado ou atualizado com sucesso.'
        )

        messages.success(
            self.request,
            'Você fez login e pode concluir sua compra.'
        )

        return redirect('perfil:criar')

class Atualizar(View):
    def get(self, *args, **kwargs):
        return render(self.request, template_name='perfil/atualizar.html')

# def login(request):
#
#     if request.method != 'POST':
#         # verifica se o formulário esta vazio
#         return redirect('perfil:criar')
#     usuario = request.POST.get('usuario')
#     senha = request.POST.get('senha')
#     # autenticar usuario
#     user = auth.authenticate(request, username=usuario, password=senha)
#     # se o usuário não autenticar, a função auth.authenticate() irá retornar None
#     if not user:
#         messages.error(request, 'Usuário ou Senha inválidos.')
#         return redirect('perfil:criar')
#     else:
#         auth.login(request, user) #faz login
#         messages.success(request, 'Voce fez login com sucesso.')
#         return redirect('produto:lista')


class Login(View):
    def post(self, *args, **kwargs):
        usuario = self.request.POST.get('usuario')
        senha = self.request.POST.get('senha')

        if not usuario or not senha:
            messages.error(
                self.request,
                'Usuário ou Senha incorretos.'
            )
            return redirect('perfil:criar')

        autentica = authenticate(
            self.request,
            username=usuario,
            password=senha
        )
        if autentica:
            login(
                self.request,
                autentica
            )
            messages.success(
                self.request,
                'Login efetuado com sucesso'
            )
            return redirect('produto:lista')


class Logout(View):
    def get(self, *args, **kwargs):
        carrinho = copy.deepcopy(self.request.session.get('carrinho'))
        self.request.session['carrinho'] = carrinho
        self.request.session.save() # Salvando carrinho na sessão para que não perdamos ele ao fazer
                                    # logout
        logout(self.request)
        return redirect('produto:lista')


class DetalhePerfil(ListView):
    """
        Detalha os dados do perfil do usuário
    """
    # TODO: IMPLEMENTAR ESSA VIEW
    model = models.Perfil
    template_name = 'perfil/detalhe.html'
    context_object_name = 'perfil'


