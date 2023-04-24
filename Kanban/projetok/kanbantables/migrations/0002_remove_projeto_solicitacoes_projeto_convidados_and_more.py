# Generated by Django 4.1.2 on 2023-04-23 22:12

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('kanbantables', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='projeto',
            name='solicitacoes',
        ),
        migrations.AddField(
            model_name='projeto',
            name='convidados',
            field=models.ManyToManyField(related_name='convidados', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AddField(
            model_name='projeto',
            name='pendentes',
            field=models.ManyToManyField(related_name='pendentes', to=settings.AUTH_USER_MODEL),
        ),
        migrations.AlterField(
            model_name='projeto',
            name='nome',
            field=models.CharField(max_length=255),
        ),
    ]
