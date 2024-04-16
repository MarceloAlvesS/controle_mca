from django.db import models
from django.contrib.auth.models import User


class Empresa(models.Model):
    choice_enquadramento = [('', '____________'),
                            ('l-m', 'Lucro Real Matriz'),
                            ('l-f', 'Lucro Real Filial'),
                            ('m', 'Mei'),
                            ('p-m', 'Presumido Matriz'),
                            ('p-f', 'Presumido Filial'),
                            ('s-m', 'Simples Matriz'),
                            ('s-f', 'Simples Filial'),
                            ('t', 'Terceiro Setor'),
                            ]
    usuarios = models.ManyToManyField(User,  related_name='empresas', through='Competencia')
    nome = models.CharField(max_length=17, blank=False,  null=False, unique=True)
    enquadramento = models.CharField(max_length=3, choices=choice_enquadramento, default='', blank=True)

    def __str__(self):
        return self.nome

class Obrigacao(models.Model):
    class Meta:
        verbose_name_plural = 'Obrigações'

    empresas = models.ManyToManyField(Empresa, related_name='obrigacoes', through='Competencia')
    usuarios = models.ManyToManyField(User, related_name='obrigacoes', through='Competencia')
    formato = models.CharField(max_length=1, choices=[('M','Mensal'),('A','Anual')], default='M')

    nome = models.CharField(max_length=17, blank=False,  null=False, unique=True)

    def __str__(self):
        return self.nome
    
class Competencia(models.Model):
    meses = ['janeiro', 'fevereiro', 'marco', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro']
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, related_name='competencias', null=True, blank=True)
    empresa = models.ForeignKey(Empresa, on_delete=models.CASCADE, related_name='competencias')
    obrigacao = models.ForeignKey(Obrigacao, on_delete=models.CASCADE, related_name='competencias')

    janeiro = models.CharField(max_length=5, blank=True, null=True)
    fevereiro = models.CharField(max_length=5, blank=True, null=True)
    marco = models.CharField(max_length=5, blank=True, null=True)
    abril = models.CharField(max_length=5, blank=True, null=True)
    maio = models.CharField(max_length=5, blank=True, null=True)
    junho = models.CharField(max_length=5, blank=True, null=True)
    julho = models.CharField(max_length=5, blank=True, null=True)
    agosto = models.CharField(max_length=5, blank=True, null=True)
    setembro = models.CharField(max_length=5, blank=True, null=True)
    outubro = models.CharField(max_length=5, blank=True, null=True)
    novembro = models.CharField(max_length=5, blank=True, null=True)
    dezembro = models.CharField(max_length=5, blank=True, null=True)
    anual = models.CharField(max_length=5, blank=True, null=True)
    obs = models.TextField(blank=True)

    def __str__(self):
        return f'{self.usuario} - {self.empresa}: {self.obrigacao}'
    