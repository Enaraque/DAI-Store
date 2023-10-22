from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Database_connection, Producto


def index(request):
    tienda_db, client = Database_connection().get_connection()
    productos_collection = Database_connection().get_collection("productos")

    consultas = get_consultas(productos_collection)
    categoriasEncabezado = get_categorias_encabezado(productos_collection)
    context = {**consultas, **categoriasEncabezado}

    return render(request, "consultas.html", context)


def get_consultas(collection):

    consulta1 = Producto.get_producto(collection,
                                      "electronics",
                                      100,
                                      200
                                      )
    consulta2 = Producto.get_product_type(collection, "pocket")
    consulta3 = Producto.get_product_by_rate(collection, 4)
    consulta4 = Producto.get_producto(collection,
                                      "men's clothing",
                                      orden="rating.rate"
                                      )
    consulta5 = Producto.get_facturacion(collection)
    consulta6 = Producto.get_facturacion(collection, "category")
    context = {
        "consulta1": consulta1,
        "consulta2": consulta2,
        "consulta3": consulta3,
        "consulta4": consulta4,
        "consulta5": consulta5,
        "consulta6": consulta6
        }
    return context


def get_categorias_encabezado(coleccion):
    categorias = Producto.get_all_categories(coleccion)
    context = {"categorias": categorias}

    return context


def get_categoria(request, categoria):
    tienda_db, client = Database_connection().get_connection()
    productos_collection = Database_connection().get_collection("productos")

    productos = Producto.get_producto(productos_collection, categoria)
    encabezado = get_categorias_encabezado(productos_collection)
    context = {"productos": productos, **encabezado}

    return render(request, "categorias.html", context)


def filtrar_busqueda(request):
    tienda_db, client = Database_connection().get_connection()
    productos_collection = Database_connection().get_collection("productos")
    filtrado = request.GET.get('search')

    productos = Producto.get_product_type(productos_collection, filtrado)
    encabezado = get_categorias_encabezado(productos_collection)
    context = {"productos": productos, **encabezado}

    return render(request, "categorias.html", context)
