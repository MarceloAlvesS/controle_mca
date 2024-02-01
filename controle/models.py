from django.db import models
from django.contrib.auth.models import User

class Empresa(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='empresas')
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome


class Obrigacao(models.Model):
    class Meta:
        verbose_name_plural = 'Obrigacoes'

    empresas = models.ManyToManyField('Empresa', related_name='obrigacoes', through='competencia')
    nome = models.CharField(max_length=50)

    def __str__(self):
        return self.nome
    
class Competencia(models.Model):
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='competencias')
    obrigacao = models.ForeignKey(Obrigacao, on_delete=models.CASCADE, related_name='competencias')
    janeiro = models.CharField(max_length=30, blank=True)
    fevereiro = models.CharField(max_length=30, blank=True)
    março = models.CharField(max_length=30, blank=True)
    abril = models.CharField(max_length=30, blank=True)
    maio = models.CharField(max_length=30, blank=True)
    junho = models.CharField(max_length=30, blank=True)
    julho = models.CharField(max_length=30, blank=True)
    agosto = models.CharField(max_length=30, blank=True)
    setembro = models.CharField(max_length=30, blank=True)
    outubro = models.CharField(max_length=30, blank=True)
    novembro = models.CharField(max_length=30, blank=True)
    dezembro = models.CharField(max_length=30, blank=True)
    obs = models.TextField(blank=True)

    def __str__(self):
        return f'{self.empresa}: {self.obrigacao}'