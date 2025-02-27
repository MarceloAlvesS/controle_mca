from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home_admin'),
    path('clientes/', views.clientes, name='clientes_admin'),
    path('clientes/<int:ano>/<str:cliente_nome>', views.cliente, name='cliente_admin'),
    path('obrigacoes/', views.obrigacoes, name='obrigacoes_admin'),
    path('obrigacoes/<int:ano>/<str:obrigacao_nome>', views.obrigacao, name='obrigacao_admin'),
    path('competencias/', views.competencias, name='competencias_admin'),
    path('competencias/<int:ano>/<str:mes>', views.competencia, name='competencia_admin'),
    path('usuarios/', views.contabil, name='contabil_admin')
]