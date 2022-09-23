from django import forms
from . import models
from django.contrib.auth.models import User

class PerfilForm(forms.ModelForm):
    class Meta:
        # model que será usado para criar o formulário
        model = models.Perfil
        # fields: Campos do model que serão incluídos no formulário, nesse caso '__all__'
        # indica que todos os campos serão incluídos no formulário
        fields = '__all__'
        # exclude: Campos que serão excluídos do formulário que iremos criar, nesse caso,
        # somente o campo 'username'
        exclude = ('usuario',)

class UserForm(forms.ModelForm):
    # O atributo abaixo faz com que não exibamos no formulário, se o usuário estiver logado
    # sua senha cadastrada no sistema, mas sim, um campo de senha padrão. As configurações
    # também incluem que, para a renovação do cadastro, o campo de senha não seja

    # password = forms.CharField(
    #     required=False,
    #     widget=forms.PasswordInput(),
    #     label='Senha'
    # )

    # Campo para confirmação da senha
    # password_confirm = forms.CharField(
    #     required=False,
    #     widget=forms.PasswordInput(),
    #     label='Confirmar Senha'
    # )

    def __init__(self, usuario=None, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Se o usuário estiver logado, saberemos que usuário enviou este formulário
        self.usuario = usuario

    class Meta:
        model = User
        fields = (
            'username',
            'first_name',
            'last_name',
            'email',
        )

    def clean(self, *args, **kwargs):
        data = self.data
        cleaned = self.cleaned_data
        validation_error_messages = {}

        print(data)

        user_data = cleaned.get('username')                     # Usuário da aplicação
        password_data = cleaned.get('password')                 # Senha da aplicação
        password_confirm_data = cleaned.get('password_confirm') # Senha de confirmação da aplicação
        email_data = cleaned.get('email')                       # Email da aplicação

        user_db = User.objects.filter(username=user_data).first() # Usuário do banco de dados
        email_db = User.objects.filter(email=email_data).first()  # Email do banco de dados

        # Configuração das mensagens de erro
        error_msg_user_exists = 'Usuário já existe.'
        error_msg_email_exists = 'E-mail já existe.'
        error_msg_password_not_match = 'As senhas digitadas não são iguais.'
        error_msg_password_short = 'A senha digitada precisa ser igual ou maior que 6 caracteres.'
        error_msg_required_field = 'Este campo é obrigatório.'


        # # Usuário logado | Atualização
        # if self.usuario:
        #     # Validação do campo 'username'
        #     if user_data != user_db:
        #         if user_db:
        #             # validation_error_messages['username'] = error_msg_user_exists
        #             pass
        #
        #     # Validação do campo 'email'
        #     if email_data != email_db:
        #         if email_db:
        #             # validation_error_messages['email'] = error_msg_email_exists
        #             pass
        #
        #     # Validação do campo 'password'
        #     if password_data:
        #
        #         # Validação de conformidade
        #         if password_data != password_confirm_data:
        #             validation_error_messages['password_confirm'] = error_msg_password_not_match
        #
        #         # Validação de tamanho
        #         if len(password_data) < 6:
        #             validation_error_messages['password'] = error_msg_password_short
        #
        # # Usuário não logado | Cadastro
        # else:
        #     # Validação do campo 'username'
        #     if user_db:
        #         validation_error_messages['username'] = error_msg_user_exists
        #     # Validação do campo 'email'
        #     if email_db:
        #         validation_error_messages['email'] = error_msg_email_exists
        #     # Validação do campo 'password'
        #     # Validação de conformidade
        #     if not password_data:
        #         validation_error_messages['password'] = error_msg_required_field
        #     # Validação de não existência do campo
        #     if not password_confirm_data:
        #         validation_error_messages['password_confirm'] = error_msg_required_field
        #
        #     if password_data != password_confirm_data:
        #         validation_error_messages['password_confirm'] = error_msg_password_not_match
        #     # Validação de tamanho
        #     if len(password_data) < 6:
        #         validation_error_messages['password'] = error_msg_password_short

        # Se existirem erros de validação na hora do cadastro de usuário
        if validation_error_messages:
            raise(forms.ValidationError(
                validation_error_messages
            ))
