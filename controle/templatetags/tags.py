from django import template
from ..models import Competencia
from django.contrib.auth.models import User

register = template.Library()

@register.simple_tag
def get_competencia_from(empresa, obrigacao, usuario, mes):
  usuario = User.objects.filter(username=usuario).first()
  competencias = Competencia.objects.filter(empresa=empresa, obrigacao=obrigacao, usuario=usuario)
  valor_mes =  competencias.values_list(mes).first()

  if valor_mes:
    if valor_mes[0]:
      return valor_mes[0]
    else:
      return ''
  else:
    return '-'