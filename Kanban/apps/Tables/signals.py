from django.db.models.signals import post_save
from django.dispatch import receiver
from django.core.exceptions import ObjectDoesNotExist
from .models import Projeto

@receiver(post_save, sender=Projeto)
def deletar_projeto_vazio(sender, instance, **kwargs):
    try:
        if not instance.dono and not instance.membros.exists() and not instance.moderadores.exists():
            instance.delete()
    except ObjectDoesNotExist:
        pass
