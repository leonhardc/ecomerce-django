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
        email_data = cleaned.get('email')                       # Email da aplicação

        user_db = User.objects.filter(username=user_data).first() # Usuário do banco de dados
        email_db = User.objects.filter(email=email_data).first()  # Email do banco de dados

        # Configuração das mensagens de erro
        error_msg_user_exists = 'Usuário já existe.'
        error_msg_email_exists = 'E-mail já existe.'

        # Se existirem erros de validação na hora do cadastro de usuário
        if validation_error_messages:
            raise(forms.ValidationError(
                validation_error_messages
            ))

# class PasswordForm(forms.ModelForm):

#     class Meta:
#         model = User
#         fields = (
#             'password',
#             'password_confirm',
#         )

#     def __init__(self, usuario=None, *args, **kwargs):
#         super().__init__(*args, **kwargs)
#         # Se o usuário estiver logado, saberemos que usuário enviou este formulário
#         self.usuario = usuario

#     def clean(self, *args, **kwargs):

#         data = self.data
#         validation_error_messages = {}

#         # Mensagens de erro
#         error_msg_password_short = 'A senha digitada precisa ser igual ou maior que 6 caracteres.'
#         error_msg_required_field = 'Este campo é obrigatório.'
#         error_msg_password_not_match = 'As senhas digitadas não são iguais.'

#         # Senha
#         password = forms.CharField(
#             required=False,
#             widget=forms.PasswordInput(),
#             label='Senha'
#         )
#         # Confirmação da senha
#         password_confirm = forms.CharField(
#             required=False,
#             widget=forms.PasswordInput(),
#             label='Confirmar Senha'
#         )

#         password_data = data.get('password')  # Senha da aplicação
#         password_confirm_data = data.get('password_confirm')  # Senha de confirmação da aplicação

#         # Verificação de senhas
#         if len(password_data) < 6:
#             validation_error_messages['password'] = error_msg_password_short

#         if password_data != password_confirm_data:
#             validation_error_messages['password_confirm'] = error_msg_password_not_match

#         # Se houver mensagens de erro, mostra no formulário
#         if validation_error_messages:
#             raise(forms.ValidationError(
#                 validation_error_messages
#             ))

