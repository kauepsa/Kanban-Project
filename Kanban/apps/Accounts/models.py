from django.db import models
from django.contrib.auth.models import AbstractUser

class Profile(AbstractUser):
    STATUS = (
        ('usuario', 'usuario'),
        ('moderador', 'moderador')
    )

    GENEROS = (
        ('MASCULINO','MASCULINO'),
        ('FEMININO','FEMININO'),
        ('OUTRO','OUTRO')
    )

    email = models.EmailField(unique=True)
    status = models.CharField(max_length=100, choices=STATUS, default='usuario')
    nome = models.CharField(max_length=100)
    idade = models.IntegerField(null=True)
    genero = models.CharField(max_length=100, choices=GENEROS, default='OUTRO')
    descricao = models.TextField('Descrição', max_length=500, default='', blank=True)
    foto_perfil = models.ImageField(upload_to='imagens/perfil/', null=True)
    linkedin = models.URLField('Linkedin', max_length=100, default='', blank=True)
    github = models.URLField('Github', max_length=100, default='', blank=True)

    def __str__(self):
        return self.username

    
