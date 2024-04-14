from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home_admin'),
    path('clientes/', views.clientes, name='clientes_admin'),
    path('clientes/<str:cliente_nome>', views.cliente, name='cliente_admin'),
    path('obrigacoes/', views.obrigacoes, name='obrigacoes_admin'),
    path('obrigacoes/<str:obrigacao_nome>', views.obrigacao, name='obrigacao_admin'),
    path('competencias/', views.competencias, name='competencias_admin'),
    path('competencias/<str:mes>', views.competencia, name='competencia_admin'),
    path('usuarios/', views.contabil, name='contabil_admin')
]