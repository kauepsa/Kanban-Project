from django.db import models
from django.contrib.auth.models import User

class Friendlist(models.Model):
    user = models.OneToOneField(User, ondelete=models.CASCADE)
    amigos = models.ManyToManyField(User, related_name='amigos')
    pendentes_enviados = models.ManyToManyField(User, related_name='Pendentes Enviados')
    pendentes_recebidos = models.ManyToManyField(User, related_name='Pendentes Recebidos')
    recusados = models.ManyToManyField(User, related_name='recusados')

class Mensagem(models.Model):
    remetente = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensagens enviadas')
    destinatario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='mensagens recebidas')
    data_envio = models.DateTimeField(auto_now_add=True)
    status = models.BooleanField(default=False)
    mensagem = models.TextField()