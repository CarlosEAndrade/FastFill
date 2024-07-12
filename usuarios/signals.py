from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import Medicos, Pacientes

@receiver(post_save, sender=Pacientes)
def create_user_for_paciente(sender, instance, created, **kwargs):
    if created:
        # Extrair cns e dn para criar username e password
        cns = instance.cns
        dn = instance.dn.strftime("%d%m%Y")  # Formatar data de nascimento como ddmmaaaa

        # Criar usuário
        user = User.objects.create_user(
            username=cns,
            password=dn,
            first_name='paciente',
            last_name=instance.paciente
        )

        # Associar o usuário ao paciente
        instance.user = user
        instance.save()


@receiver(post_save, sender=User)
def create_user_profile(sender, instance, created, **kwargs):
    if created and instance.first_name.lower() != 'paciente':
        Medicos.objects.create(user=instance)

@receiver(post_save, sender=User)
def save_user_profile(sender, instance, **kwargs):
    if instance.first_name.lower() != 'paciente' and hasattr(instance, 'medicos'):
        instance.medicos.save()

