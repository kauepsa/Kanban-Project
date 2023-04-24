from django.db import models
from django.contrib.auth.models import User

class Projeto(models.Model):
    nome = models.CharField(max_length=255)
    descricao = models.TextField()
    managers = models.ManyToManyField(User, related_name='projetos_administrados')
    users = models.ManyToManyField(User, related_name='projetos_participantes')
    convidados = models.ManyToManyField(User, related_name='convidados')
    pendentes = models.ManyToManyField(User, related_name='pendentes')

    def create_colunas_padrao(self):
        coluna_a_fazer = Coluna(nome="A Fazer", editavel=False, projeto=self)
        coluna_em_progresso = Coluna(nome="Em Progresso", editavel=False, projeto=self)
        coluna_em_revisao = Coluna(nome="Em Revisão", editavel=False, projeto=self)
        coluna_concluido = Coluna(nome="Concluído", editavel=False, projeto=self)
        coluna_a_fazer.save()
        coluna_em_progresso.save()
        coluna_em_revisao.save()
        coluna_concluido.save()


class Coluna(models.Model):
    nome = models.CharField(max_length=100)
    editavel = models.BooleanField(default=True)
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='colunas')


class Item(models.Model):
    titulo = models.CharField(max_length=100)
    descricao = models.TextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='itens')
    coluna = models.ForeignKey(Coluna, on_delete=models.CASCADE, related_name='itens')
