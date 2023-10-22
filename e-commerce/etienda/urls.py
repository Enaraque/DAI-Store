from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("categorias/<str:categoria>", views.get_categoria, name="categorias"),
    path("filtrar", views.filtrar_busqueda, name="filtro"),
    ]
