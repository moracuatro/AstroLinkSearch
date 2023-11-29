from django.urls import path
from . import views

app_name = "buscador"

urlpatterns = [
    path('', views.buscador, name='buscadorvista'),
    #path('<slug:consulta>/', views.resultado, name='consultavista'),
    path('about/', views.about),
    
]