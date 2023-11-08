from django.urls import path, include
from . import views

urlpatterns = [
    path("", views.index, name="index"),
    path("categorias/<str:categoria>", views.get_categoria, name="categorias"),
    path("filtrar", views.filtrar_busqueda, name="filtro"),
    path("nuevo_producto", views.nuevo_producto, name="nuevo_producto"),
    path(
        "nuevo_producto/insertar_nuevo_producto",
        views.insertar_nuevo_producto,
        name="insertar_nuevo_producto",
    ),
    path("login", views.get_login, name="login"),
    path("login/validar_login", views.validar_login, name="validar_login"),
    path("logout", views.get_logout, name="logout"),
]
