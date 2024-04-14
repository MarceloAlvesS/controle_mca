"""
URL configuration for controle_mca project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconfobrigacoesobrigacoes
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.urls import path
from . import views

urlpatterns = [
    
    path('', views.home, name='home'),
    path('clientes/', views.clientes),
    path('clientes/', views.clientes),
    path('clientes/<int:pagina>/', views.clientes, name='clientes'),
    path('clientes/criar/', views.criar_cliente, name='criar_cliente'),
    path('clientes/<str:cliente_nome>/', views.editar_cliente, name='editar_cliente'),
    path('obrigacoes/', views.obrigacoes),
    path('obrigacoes/<int:pagina>/', views.obrigacoes, name='obrigacoes'),
    path('obrigacoes/criar/', views.criar_obrigacao, name='criar_obrigacao'),
    path('obrigacoes/<str:obrigacao_nome>/', views.editar_obrigacao, name='editar_obrigacao'),
    path('competencias/', views.competencias, name='competencias'),
    path('competencias/<str:mes>/', views.visualizar_competencia, name='editar_competencia'),
]