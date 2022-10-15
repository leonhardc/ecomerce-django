from utils.utils import valida_cpf, calcula_idade, formata_data
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.views.generic.list import ListView
from django.contrib.auth.models import User
from django.http import HttpResponse
from django.contrib import messages
from django.views import View
from datetime import datetime
from . import models, forms
import copy
import re

# Cria usuário django com username, first_name, last_name, email, password
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
            return render(self.request, self.template_name)
        
        # Verificar se o email já está cadastrado
        if User.objects.filter(email=email):
            messages.error(
                self.request,
                'Email já existe'
            )
            return render(self.request, self.template_name)

        # Criando novo usuário django
        user = User.objects.create_user(username=novo_usuario,
                                        email=email,
                                        password=senha)
        # Login
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

# Faz login do usuário djnago depois de criado
class Login(View):
    """
        Autentica e faz login
    """

    template_login="perfil/login-signup.html"
    def get(self, *args, **kwargs):
        return render(self.request, self.template_login)


    def post(self, *args, **kwargs):
        usuario = self.request.POST.get('usuario')
        senha = self.request.POST.get('senha')

        if not usuario or not senha:
            messages.error(self.request,'Usuário ou Senha incorretos.')
            return render(self.request, self.template_login)

        autentica = authenticate(self.request, username=usuario, password=senha)
        if autentica:
            login(self.request, autentica)
            messages.success(self.request,'Login efetuado com sucesso')
            return redirect('produto:lista')
        else:
            messages.error(self.request,'Usuário ou senha inválidos')
            return render(self.request, self.template_login)

# Faz logout do usuário django quando termina a seção
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

# Atualiza dados de perfil/cadastro de usuário
class Atualizar(View):
    """
        Atualizar dados de usuário/perfil.
    """
    def __init__(self) -> None:        
        self.template_name = "perfil/atualizar.html"
        self.contexto = {}


    def get(self, *args, **kwargs):
        """
            Resgata da base de dados e carrega os dados do usuário e do perfil no formulario.
            Se não houver dados no perfil, só será carregados dados de usuário.        """
        perfil = models.Perfil.objects.filter(usuario = self.request.user).first()
        if perfil:
                self.contexto = {
                    'userform': forms.UserForm(
                        data=self.request.POST or None,
                        usuario=self.request.user,
                        instance=self.request.user
                    ),
                    'perfilform': forms.PerfilForm(
                        instance=perfil
                    )
                }
        else:
            self.contexto = {
            'userform': forms.UserForm(
                data=self.request.POST or None,
                usuario=self.request.user,
                instance=self.request.user
            ),
            'perfilform': forms.PerfilForm()
        }


        return render(self.request, self.template_name, self.contexto)


    def post(self, *args, **kwargs):
        """
            Resgada os dados dos formulario de Usuário e de Perfil e salva na base de dados.
        """
        # Atualizando dados de usuário. 
        user = User.objects.get(username = self.request.user)        
        perfil = models.Perfil.objects.filter(usuario = self.request.user).first()
        
        if perfil:
                self.contexto = {
                    'userform': forms.UserForm(
                        data=self.request.POST or None,
                        usuario=self.request.user,
                        instance=self.request.user
                    ),
                    'perfilform': forms.PerfilForm(
                        instance=perfil
                    )
                }
        else:
            self.contexto = {
            'userform': forms.UserForm(
                data=self.request.POST or None,
                usuario=self.request.user,
                instance=self.request.user
            ),
            'perfilform': forms.PerfilForm()
        }

        # Resgatando dados do formulario de usuário
        usuario = self.request.POST.get('username')
        email = self.request.POST.get('email')
        nome = self.request.POST.get('first_name')
        sobrenome = self.request.POST.get('last_name')

        # Salvando dados de usuário no banco de dados
        # Verficação da existencia do usuário no banco de dados
        query_user = User.objects.get(username = usuario)
        if usuario != user.username and query_user:
               
            messages.error(
                self.request,
                'Usuário já existe'
            )
            return render(
                self.request,
                template_name=self.template_name,
                context=self.contexto
            )
        else:
            # salvar novo username e relogar o usuário
            pass

        user.email = email
        user.first_name = nome
        user.last_name = sobrenome
        user.save()
        
        ## Salvando dados de perfil ##

        # Resgatando dados do formulario
        bairro = self.request.POST.get('bairro')
        cep = self.request.POST.get('cep')
        cidade = self.request.POST.get('cidade')
        complemento = self.request.POST.get('complemento')
        cpf = self.request.POST.get('cpf')
        data_nascimento = self.request.POST.get('data_nascimento')
        endereco = self.request.POST.get('endereco')
        estado = self.request.POST.get('estado')
        idade = self.request.POST.get('idade')
        numero = self.request.POST.get('numero')
        
        # Verificações de integridade dos dados
        if not valida_cpf(cpf):
            messages.error(self.request,'CPF inválido')
            return render(self.request, self.template_name, self.contexto)

        idade_log = calcula_idade(datetime.strptime(data_nascimento, "%d/%m/%Y").date())
        if int(idade) != idade_log:
            idade = idade_log

        if len(cep) < 8:
            messages.error(self.request, 'CEP inválido')
            return render(self.request, self.template_name, self.contexto)
        
        if datetime.strptime(data_nascimento, "%d/%m/%Y") > datetime.today():
            messages.error(self.request, 'Data de Nascimento não pode ser maior do que data atual.')
            return render(self.request, self.template_name, self.contexto)
  
        # fim das verificações

        if perfil:
            # Salvar dados do formulario de perfil no banco de dados
            perfil.data_nascimento = formata_data(data_nascimento)
            perfil.complemento = complemento
            perfil.endereco = endereco
            perfil.cidade = cidade
            perfil.bairro = bairro
            perfil.estado = estado
            perfil.numero = numero
            perfil.usuario = user
            perfil.idade = idade
            perfil.cep = cep
            perfil.cpf = cpf
        else:
            perfil = models.Perfil(
                data_nascimento = formata_data(data_nascimento),
                complemento = complemento,
                endereco = endereco,
                cidade = cidade,
                bairro = bairro,
                estado = estado,
                numero = numero,
                usuario = user,
                idade =idade,
                cep = cep,
                cpf = cpf
            )

        perfil.save()        

        messages.success(self.request, 'Usuário salvo com sucesso')
        return redirect( 'produto:lista')

# Mostra os detalhes do perfil no template
class DetalhePerfil(ListView):
    """
        Detalha os dados do perfil do usuário
    """
    model = models.Perfil
    template_name = 'perfil/detalhe.html'
    context_object_name = 'perfil'

# Deleta usuário da base de dados
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

# Atualiza senha do usuário
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
