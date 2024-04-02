from django.urls import path
from . import views

urlpatterns = [
    path('', views.login, name='login'),
    path('cadastrar/', views.cadastrar, name='cadastrar'),
    path('user/', views.usuario, name='usuario'),
    path('user/password/', views.alterar_password, name='senha'),
    path('user/username', views.alterar_username, name='nome'),
    path('logout/', views.logout, name='logout'),
]