from django.db import models

from django.contrib.auth.models import User

class Perfil(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    nome = models.CharField(max_length=100)
    idade = models.IntegerField()
    genero = models.CharField(max_length=100)
    descricao = models.CharField(max_length=500, null=True)
    useremail = models.EmailField(max_length=100)
    foto_perfil = models.ImageField(upload_to='imagens/perfil/', null=True)
    foto_banner = models.ImageField(upload_to='imagens/banner/', null=True)
    linkedin = models.URLField(null=True)
    github = models.URLField(null=True)

    def __str__(self):
        return self.nome
