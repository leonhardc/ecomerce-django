from django.db import models
from django.contrib.auth.models import User
from django.forms import ValidationError
from utils.utils import valida_cpf
from PIL import Image
import os
import re


class Perfil(models.Model):

    usuario = models.OneToOneField(User, on_delete=models.CASCADE) # se o usuário for apagado, o perfil 
                                                                   # também será apagado
    foto_perfil = models.ImageField(
        upload_to='perfil_photo/%Y/%m/',
        blank= True,
        null= True)
    
    idade = models.PositiveIntegerField()
    data_nascimento = models.DateField()
    cpf = models.CharField(max_length=11)
    
    endereco = models.CharField(max_length=50)
    numero = models.CharField(max_length=5)
    complemento = models.CharField(max_length=30)
    bairro = models.CharField(max_length=30)
    cep = models.CharField(max_length=8)
    cidade = models.CharField(max_length=30)
    estado = models.CharField(
        max_length=2,
        default='CE',
        choices= (
            ('AC', 'Acre'),
            ('AL', 'Alagoas'),
            ('AP', 'Amapá'),
            ('AM', 'Amazonas'),
            ('BA', 'Bahia'),
            ('CE', 'Ceará'),
            ('DF', 'Distrito Federal'),
            ('ES', 'Espírito Santo'),
            ('GO', 'Goiás'),
            ('MA', 'Maranhão'),
            ('MT', 'Mato Grosso'),
            ('MS', 'Mato Grosso do Sul'),
            ('MG', 'Minas Gerais'),
            ('PA', 'Pará'),
            ('PB', 'Paraíba'),
            ('PR', 'Paraná'),
            ('PE', 'Pernambuco'),
            ('PI', 'Piauí'),
            ('RJ', 'Rio de Janeiro'),
            ('RN', 'Rio Grande do Norte'),
            ('RS', 'Rio Grande do Sul'),
            ('RO', 'Rondônia'),
            ('RR', 'Roraima'),
            ('SC', 'Santa Catarina'),
            ('SP', 'São Paulo'),
            ('SE', 'Sergipe'),
            ('TO', 'Tocantins'),
        )
    )

    @staticmethod
    def resize_image(img, max_width=800):
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name) # caminho completo da imagem
        image_pil = Image.open(img_full_path) # abrir imagem com pil
        original_width, original_height = image_pil.size # altura e largura original da imagem

        if original_width <= max_width:
            image_pil.close() # fechando a imagem aberta anteriormente
            return # se a largura original for menor que a nova largura, não precisa
                   # fazer o redimensionamento

        new_height = round((max_width * original_height) / original_width) # descobrir nova altura
        new_image = image_pil.resize((max_width, new_height), Image.LANCZOS) # redimensiona imagem
        new_image.save(         # salva a nova imagem por cima da antiga
            img_full_path,      # onde se deseja salvar a imagem
            optimize=True,
            quality=50          # reduz a qualidade para 50%
        )

    def __str__(self):
        return f'{self.usuario.first_name}'

    def clean(self):
        error_messages = {}

        if not valida_cpf(self.cpf):
            error_messages['cpf'] = 'Digite um cpf válido'

        if len(self.cep) < 8: # TODO: fazer uma validação de cpf mais forte
            error_messages['cep'] = 'CEP inválido, digite apenas números'

        # Depois de validar todos os campos
        if error_messages:
            raise ValidationError(error_messages)

    class Meta:
        verbose_name = 'Perfil'
        verbose_name_plural = 'Perfis'


