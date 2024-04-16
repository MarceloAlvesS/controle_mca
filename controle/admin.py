from django.contrib import admin
from .models import *

class CompetenciaAdmin(admin.ModelAdmin):
    list_display = ('empresa', 'obrigacao', 'usuario', 'janeiro', 'fevereiro', 'marco', 'abril', 'maio', 'junho', 'julho', 'agosto', 'setembro', 'outubro', 'novembro', 'dezembro')
    ordering = ('empresa',)

class EmpresaAdmin(admin.ModelAdmin):
    list_display = ('nome', )

admin.site.register(Empresa, EmpresaAdmin)
admin.site.register(Obrigacao)
admin.site.register(Competencia, CompetenciaAdmin)
