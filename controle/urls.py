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
    path('empresas/', views.empresas),
    path('empresas/<int:pagina>/', views.empresas, name='empresas'),
    path('empresas/<str:empresa>/', views.empresa, name='empresa'),
    path('obrigacoes/', views.obrigacoes),
    path('obrigacoes/<int:pagina>/', views.obrigacoes, name='obrigacoes'),
    path('obrigacoes/<str:obrigacao>/', views.obrigacao, name='obrigacao'),
    path('competencias/', views.competencias),
    path('competencias/<int:pagina>/', views.competencias, name='competencias'),
    path('competencias/<str:competencia>/', views.competencia, name='competencia'),
]