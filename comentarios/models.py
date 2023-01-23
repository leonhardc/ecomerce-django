from django.db import models
from produto.models import Produto
from django.contrib.auth.models import User  # para usuario_comentario
from django.utils import timezone  # para data_comentario


class Comentario(models.Model):
    comentario = models.TextField(verbose_name='Comentario')
    produto_comentario = models.ForeignKey(Produto, on_delete=models.CASCADE, verbose_name='Produto ID')
    usuario_comentario = models.ForeignKey(User, on_delete=models.DO_NOTHING, verbose_name='Autor ID', blank=True, null=True)
    data_comentario = models.DateTimeField(default=timezone.now, verbose_name='Publicado em')
    publicado_comentario = models.BooleanField(default=True, verbose_name='Publicar')



