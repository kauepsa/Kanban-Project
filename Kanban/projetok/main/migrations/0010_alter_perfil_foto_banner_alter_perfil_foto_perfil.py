# Generated by Django 4.1.2 on 2023-04-22 13:25

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('main', '0009_alter_perfil_foto_banner_alter_perfil_foto_perfil'),
    ]

    operations = [
        migrations.AlterField(
            model_name='perfil',
            name='foto_banner',
            field=models.ImageField(null=True, upload_to='imagens/banner/'),
        ),
        migrations.AlterField(
            model_name='perfil',
            name='foto_perfil',
            field=models.ImageField(null=True, upload_to='imagens/perfil/'),
        ),
    ]
