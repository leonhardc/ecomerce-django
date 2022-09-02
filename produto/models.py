from django.db import models
from django.conf import settings
from PIL import Image
import os

class Produto(models.Model):
    nome = models.CharField(max_length=255)
    descricao_curta = models.TextField(max_length=255)
    descricao_longa = models.TextField()
    imagem = models.ImageField(
        upload_to='produto_imagens/%Y/%m/',
        blank= True,
        null= True
    )
    slug = models.SlugField(unique=True)
    preco_marketing = models.FloatField()
    preco_marketing_promocional = models.FloatField(default=0)
    tipo = models.CharField(
        default='V',
        max_length=1,
        choices=(
            ('V', 'Variação'),
            ('S', 'Simples')
        )
    )

    #  Redimensionar imagem antes de salvar
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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        max_image_size = 800

        if self.imagem:
            self.resize_image(self.imagem, max_image_size)

    def __str__(self):
        return self.nome

class Variacao(models.Model):
    produto = models.ForeignKey(Produto, on_delete=models.CASCADE)
    nome = models.CharField(
        max_length=50,
        blank=True,
        null=True
    )
    preco = models.FloatField()
    preco_promocional = models.FloatField(default=0)
    estoque = models.PositiveIntegerField(default=1)

    def __str__(self):
        return self.nome or self.produto.nome

    class Meta:
        verbose_name = 'Variação'
        verbose_name_plural = 'Variações'
