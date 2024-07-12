from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name="home"),
    path('cadastro/', views.cadastro, name="cadastro"),
    path('addpac/', views.addpac, name="addpac"),
    path('paciente/', views.paciente, name='paciente'),
    path('apacoff/', views.apacoff, name='apacoff'),
    path('sisregoff/', views.sisregoff, name='sisregoff'),

]


