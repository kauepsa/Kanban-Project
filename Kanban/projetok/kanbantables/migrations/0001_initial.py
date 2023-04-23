# Generated by Django 4.1.2 on 2023-04-22 13:25

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Coluna',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('editavel', models.BooleanField(default=True)),
            ],
        ),
        migrations.CreateModel(
            name='Projeto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nome', models.CharField(max_length=100)),
                ('descricao', models.TextField()),
                ('managers', models.ManyToManyField(related_name='projetos_administrados', to=settings.AUTH_USER_MODEL)),
                ('solicitacoes', models.ManyToManyField(related_name='projetos_solicitados', to=settings.AUTH_USER_MODEL)),
                ('users', models.ManyToManyField(related_name='projetos_participantes', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Item',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=100)),
                ('descricao', models.TextField()),
                ('coluna', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens', to='kanbantables.coluna')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='itens', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.AddField(
            model_name='coluna',
            name='projeto',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='colunas', to='kanbantables.projeto'),
        ),
    ]
