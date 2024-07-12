from django.db import models
from django.contrib.auth.models import User
from django.conf import settings
import os
from cema.cripto import encrypt, decrypt
from datetime import datetime, timedelta
from django.utils import timezone


class Pacientes(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    paciente = models.CharField(max_length=150)
    cns = models.CharField(max_length=15)
    mae = models.CharField(max_length=150)
    sexo = models.CharField(max_length=1, choices=[("M",'Masculino'), ("F", 'Feminino')], default="M")
    raca = models.CharField(max_length=15)
    dn = models.DateField()
    tipagem = models.CharField(max_length=15)
    nacionalidade = models.CharField(max_length=30)
    naturalidade = models.CharField(max_length=30)
    cidade= models.CharField(max_length=30)
    
    def __str__(self):
        return self.paciente

    def riscoOK(self):
        seisM = timezone.now() - timedelta(days=180)
        return self.riscos.filter(data__gte=seisM).exists()


class Riscos(models.Model):
    paciente = models.ForeignKey(Pacientes, related_name='riscos', on_delete=models.CASCADE)
    resultado = models.CharField(max_length=50)
    data = models.DateField()
    obs = models.CharField(max_length=50)
    apto = models.BooleanField() 
    uti = models.BooleanField()

    def __str__(self):
        return self.data

class Comorbidades(models.Model):
    paciente = models.ForeignKey(Pacientes, related_name='comorbidades', on_delete=models.CASCADE)
    comorbidade = models.CharField(max_length=50)
    medicacao = models.CharField(max_length=50)

    def __str__(self):
        return self.comorbidade
    

class Telefones(models.Model):
    paciente = models.ForeignKey(Pacientes, related_name='telefones', on_delete=models.CASCADE)
    telefone = models.CharField(max_length=15)
    nomecontato = models.CharField(max_length=15)

    def __str__(self):
        return f"{self.telefone} ({self.nomecontato})"


class Especialidades(models.Model):
    especialidade = models.CharField(max_length=100)
    icone = models.ImageField(upload_to="icones", null=True, blank=True)

    def __str__(self):
        return self.especialidade


class Medicos(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    matricula = models.CharField(max_length=10)
    crm = models.CharField(max_length=10)
    cns = models.CharField(max_length=15)
    celular = models.CharField(max_length=15, default="")
    trak = models.CharField(max_length=256)
    sisreg = models.CharField(max_length=100) 
    sisrep = models.CharField(max_length=256)
    especialidade = models.ForeignKey(Especialidades, on_delete=models.DO_NOTHING, null=True, blank=True)


    def save(self, *args, **kwargs):
        if self.trak:
            self.trak = encrypt(self.trak)
        if self.sisrep:
            self.sisrep = encrypt(self.sisrep)
        super().save(*args, **kwargs)

    def get_trak(self):
        if self.trak:
            return decrypt(self.trak)
        return None

    def get_sisrep(self):
        if self.sisrep:
            return decrypt(self.sisrep)
        return None
