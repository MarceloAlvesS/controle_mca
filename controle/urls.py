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
    path('login/', views.login, name='login'),
    path('cadastrar/', views.cadastrar, name='cadastrar'),
    path('user/', views.usuario, name='usuario'),
    path('user/password/', views.alterar_password, name='senha'),
    path('user/username', views.alterar_username, name='nome'),
    path('logout/', views.logout, name='logout'),
    path('', views.home, name='home'),
    path('empresas/', views.empresas),
    path('empresas/<int:pagina>/', views.empresas, name='empresas'),
    path('empresas/criar/', views.empresa_criar, name='criar_empresa'),
    path('empresas/<str:empresa>/', views.empresa_view, name='empresa'),
    path('obrigacoes/', views.obrigacoes),
    path('obrigacoes/<int:pagina>/', views.obrigacoes, name='obrigacoes'),
    path('obrigacoes/<str:obrigacao>/', views.obrigacao_view, name='obrigacao'),
    path('competencias/', views.competencias, name='competencias'),
    path('competencias/<str:competencia>/', views.competencia, name='competencia'),
]