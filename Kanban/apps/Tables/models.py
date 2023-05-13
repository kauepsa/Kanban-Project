from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()

class Projeto(models.Model):
    titulo = models.CharField(max_length=255, unique=True)
    descricao = models.TextField()
    prazo = models.DateTimeField()
    criado_em = models.DateTimeField(auto_now_add=True)
    dono = models.ForeignKey(User, on_delete=models.CASCADE, related_name='projetos_criados')
    moderadores = models.ManyToManyField(User, related_name='projetos_moderados', blank=True)
    membros = models.ManyToManyField(User, related_name='projetos_membros', blank=True)
    publico = models.BooleanField(default=False)
    solicitacoes_entrada = models.ManyToManyField(User, related_name='solicitacoes_entrada', blank=True)
    convites_pendentes = models.ManyToManyField(User, related_name='convites_pendentes', blank=True)
    convites_enviados = models.ManyToManyField(User, related_name='convites_enviados', blank=True)

    def save(self, *args, **kwargs):
        if not self.pk:
            super(Projeto, self).save(*args, **kwargs)

            Coluna.objects.create(projeto=self, nome='Planejamento', editavel=False)
            Coluna.objects.create(projeto=self, nome='Andamento', editavel=False)
            Coluna.objects.create(projeto=self, nome='Revisão', editavel=False)
            Coluna.objects.create(projeto=self, nome='Completo', editavel=False)
        else:
            super(Projeto, self).save(*args, **kwargs)

    def __str__(self):
        return self.titulo



class Coluna(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE, related_name='colunas')
    nome = models.CharField(max_length=255)
    itens = models.ManyToManyField('Item', related_name='colunas')
    editavel = models.BooleanField(default=True)

    def __str__(self):
        return self.nome

class Item(models.Model):
    projeto = models.ForeignKey(Projeto, on_delete=models.CASCADE)
    coluna = models.ForeignKey(Coluna, on_delete=models.CASCADE, related_name='itens_coluna')
    titulo = models.CharField(max_length=255)
    descricao = models.TextField(blank=True, null=True)
    criado_por = models.ForeignKey(User, on_delete=models.CASCADE)

    criado_em = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.titulo

