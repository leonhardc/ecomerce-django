from django.db import models
from produto.models import Produto
from django.contrib.auth.models import User  # para usuario_comentario
from django.utils import timezone  # para data_comentario


class Comentario(models.Model):
    nome_comentario = models.CharField(max_length=150, verbose_name='Nome')
    email_comentario = models.EmailField(verbose_name='Email')
    comentario = models.TextField(verbose_name='Comentario')
    produto_comentario = models.ForeignKey(Produto, on_delete=models.CASCADE, verbose_name='Produto ID')
    usuario_comentario = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Autor ID', blank=True, null=True)
    data_comentario = models.DateTimeField(default=timezone.now, verbose_name='Publicado em')
    publicado_comentario = models.BooleanField(default=False, verbose_name='Publicar')



