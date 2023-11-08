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
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login, logout

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
    context = {
        "consulta1": consulta1,
        "consulta2": consulta2,
        "consulta3": consulta3,
        "consulta4": consulta4,
        "consulta5": consulta5,
        "consulta6": consulta6,
    }
    return context


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

    context = {"categorias": categorias}

    return context


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
                imagen.name = (
                    name + "-" + dt.utcnow().strftime("%Y%m%d%H%M%S") + extension
                )
                print(imagen.name)

                with Image.open(imagen) as img:
                    img.save(f"static/img/{imagen.name}")
            else:
                imagen = None

            print(type(imagen))
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

            productos_collection = DB.get_collection("productos")
            encabezado = get_categorias_encabezado(productos_collection)
            context = {**encabezado}

            messages.success(request, "Producto agregado correctamente")

            return render(request, "landing_page.html", context)

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
    tienda_db, client = DB.get_connection()
    productos_collection = DB.get_collection("productos")

    encabezado = get_categorias_encabezado(productos_collection)
    form = LogginForm()
    context = {**encabezado, "form": form}

    if request.method == "POST":
        form = LogginForm(request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return render(request, "landing_page.html", context)

            else:
                messages.error(request, "Usuario o contraseña incorrectos")
                return render(request, "registration/login.html", context)

    return render(request, "registration/login.html", context)


def get_logout(request):
    tienda_db, client = DB.get_connection()
    productos_collection = DB.get_collection("productos")

    encabezado = get_categorias_encabezado(productos_collection)
    context = {**encabezado}

    logout(request)
    messages.success(request, "Sesión cerrada correctamente")
    return render(request, "landing_page.html", context)
