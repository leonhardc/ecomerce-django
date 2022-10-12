from email import message
from django.http import HttpResponse
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.contrib import messages
from django.views import View
from . import models, forms
import re
import copy

class BasePerfil(View):
    template_name = 'perfil/login-signup.html'

    def setup(self, *args, **kwargs):  # Início do setup()
        """ 
            Indica funcionamento básico das variáveis de instância das classes filhas que manipulam
            o perfil de usuário    
        """
        super().setup(*args, **kwargs)

        self.carrinho = copy.deepcopy(self.request.session.get('carrinho', {}))
        self.perfil = None

        if self.request.user.is_authenticated:  # Para usuário autenticado
            # 1. Muda template_name para o template de criar ou atualizar um perfil
            self.template_name = 'perfil/criar.html'

            # 2. Verifica se há algum registro de perfil com determinada instância de usuário
            self.perfil = models.Perfil.objects.filter(
                usuario=self.request.user
            ).first()

            # 3. Formata contexto para usuário autenticado
            self.contexto = {
                'userform': forms.UserForm(
                    data=self.request.POST or None,
                    usuario=self.request.user,
                    instance=self.request.user
                ),
                'perfilform': forms.PerfilForm(
                    data=self.request.POST or None,
                    instance=self.perfil
                )
            }
        else:  # Para usuário não autenticado
            # Formata contexto para usuário não autenticado
            self.contexto = {
                'userform': forms.UserForm(data=self.request.POST or None),
                'perfilform': forms.PerfilForm(data=self.request.POST or None)
            }

        self.userform = self.contexto['userform']
        self.perfilform = self.contexto['perfilform']

        # Renderizar template
        self.renderizar = render(
            self.request,
            self.template_name,
            self.contexto
        )

    # Final do setup()

    def get(self, *args, **kwargs):
        """ Retorna template correto já renderizado """
        return self.renderizar
        

class Criar(BasePerfil):
    """
        Cria perfil de usuário
    """
    def post(self, *args, **kwargs):

        # Validação para formulário de usuário
        if not self.userform.is_valid():
            messages.error(
                self.request,
                'Formulário Invalido'
            )
            return self.renderizar

        # Se o formulário de usuário for válido, faça tudo que está abaixo
        # LEMBRETE: Este formulário não deve atualizar senha
        username = self.userform.cleaned_data.get('username')
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
            usuario.email = email
            usuario.first_name = first_name
            usuario.last_name = last_name
            usuario.save()

            # Validação para perfil
            if not self.perfil:
                perfil = models.Perfil(**self.perfilform.cleaned_data)
                perfil.usuario = usuario
                perfil.save()

            else:
                perfil = self.perfilform.save(commit=False)
                perfil.usuario = usuario
                perfil.save()
                

        # Salva o carrinho na sessão
        self.request.session['carrinho'] = self.carrinho
        self.request.session.save()

        messages.success(
            self.request,
            'Seu cadastro foi criado ou atualizado com sucesso.'
        )

        if self.request.session['carrinho']:
            messages.success(
                self.request,
                'Você fez login e pode concluir sua compra.'
            )

        return redirect('perfil:detalheperfil')


class CriarUsuario(View):

    template_name = 'perfil/cadastro_ou_pagprincipal.html'

    def post(self, *args, **kwargs):
        novo_usuario = self.request.POST.get('newuser')
        email = self.request.POST.get('email')
        senha = self.request.POST.get('pswd')
        self.carrinho = copy.deepcopy(self.request.session.get('carrinho'), {})
        self.request.session.save()

        # Verificar se o usuário já está cadastrado
        if User.objects.filter(username=novo_usuario):
            messages.error(
                self.request,
                'Usuário já existe'
            )
            return redirect('perfil:criar')
        # Verificar se o email já está cadastrado
        if User.objects.filter(email=email):
            messages.error(
                self.request,
                'Email já existe'
            )
            return redirect('perfil:criar')

        # Criando novo usuário django
        user = User.objects.create_user(username=novo_usuario,
                                        email=email,
                                        password=senha)
        # Fazer login
        autentica = authenticate(
            self.request,
            username=novo_usuario,
            password=senha
        )
        if autentica:
            login(
                self.request,
                autentica
            )
        return render(self.request, self.template_name)


class ValidarUsuario(BasePerfil):
    def post(self, *args, **kwargs):
        if not self.userform.is_valid():  # Se o formulário é válido

            username = self.userform.cleaned_data.get('username')
            password = self.userform.cleaned_data.get('password')
            email = self.userform.cleaned_data.get('email')
            first_name = self.userform.cleaned_data.get('first_name')
            last_name = self.userform.cleaned_data.get('last_name')

            if self.request.user.is_authenticated:
                usuario = get_object_or_404(
                    User,
                    username=self.request.user.username
                )

                usuario.username = username

                usuario.email = email
                usuario.first_name = first_name
                usuario.last_name = last_name
                usuario.save()

        else:  # Se o formulário de usuário não for válido
            messages.error(
                self.request,
                'Formulario Invalido'
            )
            return self.renderizar


class Login(View):
    """
        Autentica e faz login
    """

    template_login="perfil/login-signup.html"
    def get(self, *args, **kwargs):
        return redirect('perfil:criar')


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
        else:
            messages.error(
                self.request,
                'Usuário ou senha inválidos'
            )
            return render(self.request, self.template_login)


class Logout(View):
    """
        Faz logout e salva o carrinho de compras.
    """
    def get(self, *args, **kwargs):
        carrinho = copy.deepcopy(self.request.session.get('carrinho'))
        self.request.session['carrinho'] = carrinho
        self.request.session.save()  # Salvando carrinho na sessão para que não perdamos ele ao fazer
        # logout
        logout(self.request)
        return redirect('produto:lista')


class Atualizar(View):
    """
        Atualizar dados de usuário/perfil.
    """
    def get(self, *args, **kwargs):
        return redirect('perfil:criar')


class DetalhePerfil(ListView):
    """
        Detalha os dados do perfil do usuário
    """
    model = models.Perfil
    template_name = 'perfil/detalhe.html'
    context_object_name = 'perfil'


class DeletarUsuário(View):
    """
        Esta view deleta o usuário logado.
    """

    @login_required(redirect_field_name='login')
    def get(self, *args, **kwargs):

        if self.request.user.is_authenticated:
            user = User.objects.filter(username=self.request.user)
            self.request.session.get('carrinho').clear()
            self.request.session.save()
            user.delete()
            messages.success(
                self.request,
                'Usuário deletado com sucesso'
            )
            return redirect('produto:lista')
        else:
            messages.error(
                self.request,
                'Usuário não existe'
            )
            return redirect('produto:lista')


class AtualizarSenha(View):
    """
        Esta view verifica e valida a nova senha de usuário com base
        em quatro requisitos:
            1. A nova senha deve ter um tamanho mínimo de 6 caracteres;
            2. A nova senha deve ser confirmada duas vezes;
            3. A nova senha deve ser diferente da senha antiga;
            4. A nova senha deve ter numeros e letras (minusculas);
        Se todos os requisitos forem satisfeitos, a senha será atualizada.
    """
    template_atualizar_senha="perfil/atualizar_senha.html"
    template_login="perfil/login-signup.html"

    # def post(self, *args, **kwargs):
    #     contexto = {'passwordform': forms.PasswordForm}
    #     return render(self.request, self.template_atualizar_senha, contexto)


    def post(self, *args, **kwargs):
        nova_senha = self.request.POST.get('password')
        nova_senha_confirm = self.request.POST.get('password-confirm')
        user = User.objects.get(username=self.request.user.username)

        # REQUISITO: A senha deve ter mais que 6 caracteres
        if len(nova_senha) < 6:
            messages.error(
                self.request,
                'Senha precisar ter, pelo menos, seis caracteres'
            )
            return render(self.request, self.template_atualizar_senha)
        # REQUISITO: O conteudo do campo senha, deve ser o mesmo do campo de confirmação de senha
        if nova_senha != nova_senha_confirm:
            messages.error(
                self.request,
                'As senhas precisam ser iguais'
            )
            return render(self.request, self.template_atualizar_senha)
        # REQUISITO: A nova senha deve ser diferente da senha antiga
        if user.check_password(nova_senha):
            messages.error(
                self.request,
                'A nova senha deve ser diferente da senha antiga.'
            )
            return render(self.request, self.template_atualizar_senha)
        # REQUISITO: Nova senha deve conter letrar e numeros
        if (not re.search(r'[0-9]', nova_senha)) or (not re.search(r'[a-z]', nova_senha)):
            messages.error(
                self.request,
                'A senha deve conter letras e numeros.'
            )
            return render(self.request, self.template_atualizar_senha)
        
        user.set_password(nova_senha)
        user.save()
        messages.success(
            self.request,
            'Senha Alterada com sucesso. Faça Login novamente.'
        )
        return render(self.request, self.template_login)

    def get(self, *args, **kwargs):   
             
        return render(
            self.request,
            self.template_atualizar_senha
        )
