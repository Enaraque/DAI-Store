from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Database_connection as DB, Producto
from .forms import ProductoForm, LogginForm
from django.contrib import messages
import logging
from PIL import Image
from datetime import datetime as dt
import os
from datetime import timezone
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

from django.shortcuts import redirect


logger = logging.getLogger(__name__)


def index(request):
    tienda_db, client = DB.get_connection()
    productos_collection = DB.get_collection("productos")

    categorias = get_categorias_encabezado(productos_collection)
    context = {**categorias}

    return render(request, "landing_page.html", context)


def get_consultas(colection):
    consulta1 = Producto.get_producto(colection, "electronics", 100, 200)
    consulta2 = Producto.get_product_type(colection, "pocket")
    consulta3 = Producto.get_product_by_rate(colection, 4)
    consulta4 = Producto.get_producto(colection, "men's clothing", orden="rating.rate")
    consulta5 = Producto.get_facturacion(colection)
    consulta6 = Producto.get_facturacion(colection, "category")
    return {
        "consulta1": consulta1,
        "consulta2": consulta2,
        "consulta3": consulta3,
        "consulta4": consulta4,
        "consulta5": consulta5,
        "consulta6": consulta6,
    }


def get_categorias_encabezado(coleccion):
    categoriasEncabezado = Producto.get_all_categories(coleccion)
    imagenes = get_imagen_categoria(coleccion, categoriasEncabezado)

    categorias = []
    for i in range(len(categoriasEncabezado)):
        categoria_con_imagen = {
            "nombre": categoriasEncabezado[i],
            "imagen": imagenes[i],
        }
        categorias.append(categoria_con_imagen)

    return {"categorias": categorias}


def get_imagen_categoria(coleccion, categorias):
    imagenes = []
    for categoria in categorias:
        productos = Producto.get_producto(coleccion, categoria)
        imagen = Producto.get_imagen_producto(coleccion, productos[0]["_id"])
        imagenes.append(imagen["image"])

    return imagenes


def get_categoria(request, categoria):
    tienda_db, client = DB.get_connection()
    productos_collection = DB.get_collection("productos")

    productos = Producto.get_producto(productos_collection, categoria)
    encabezado = get_categorias_encabezado(productos_collection)
    context = {"productos": productos, **encabezado}

    return render(request, "categorias.html", context)


def filtrar_busqueda(request):
    tienda_db, client = DB.get_connection()
    productos_collection = DB.get_collection("productos")
    filtrado = request.GET.get("search")

    productos = Producto.get_product_type(productos_collection, filtrado)
    encabezado = get_categorias_encabezado(productos_collection)
    context = {"productos": productos, **encabezado}

    return render(request, "categorias.html", context)


def nuevo_producto(request):
    tienda_db, client = DB.get_connection()
    productos_collection = DB.get_collection("productos")
    form = ProductoForm()
    encabezado = get_categorias_encabezado(productos_collection)
    context = {**encabezado, "form": form}

    return render(request, "nuevo_producto.html", context)


def insertar_nuevo_producto(request):
    tienda_db, client = DB.get_connection()
    productos_collection = DB.get_collection("productos")

    encabezado = get_categorias_encabezado(productos_collection)
    context = {**encabezado}

    if request.method == "POST":
        form = ProductoForm(request.POST, request.FILES)
        if form.is_valid():
            nombre = form.cleaned_data["nombre"]
            precio = form.cleaned_data["precio"]
            descripcion = form.cleaned_data["descripcion"].capitalize()
            categoria = form.cleaned_data["categoria"]
            if "imagen" in request.FILES:
                imagen = request.FILES["imagen"]
                name, extension = os.path.splitext(imagen.name)
                imagen.name = "".join(
                    (
                        name
                        + "-"
                        + dt.now(timezone.utc).strftime("%Y%m%d%H%M%S")
                        + extension
                    ).split()
                )

                with Image.open(imagen) as img:
                    img.save(f"static/img/{imagen.name}")
            else:
                imagen = None

            rating = {"rate": 0.0, "count": 1}
            datos = {
                "title": nombre,
                "price": precio,
                "description": descripcion,
                "category": categoria,
                "image": str(imagen),
                "rating": rating,
            }
            Producto.add_producto(productos_collection, datos)

            messages.success(request, "Producto agregado correctamente")
            return redirect("index")

        context = {**encabezado, "form": form}

    return render(request, "nuevo_producto.html", context)


def get_login(request):
    tienda_db, client = DB.get_connection()
    productos_collection = DB.get_collection("productos")

    encabezado = get_categorias_encabezado(productos_collection)
    form = LogginForm()
    context = {**encabezado, "form": form}

    return render(request, "registration/login.html", context)


def validar_login(request):
    if request.method == "POST":
        form = LogginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect("index")
            else:
                messages.error(request, "Usuario o contraseña incorrectos")
    return redirect("login")


def get_logout(request):
    logout(request)
    messages.success(request, "Sesión cerrada correctamente")
    return redirect("index")
