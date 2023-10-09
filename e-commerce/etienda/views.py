from django.shortcuts import render
from django.http import HttpResponse
from django.template import loader
from .models import Database_connection, Producto


def index(request):
    template = loader.get_template("consultas.html")
    tienda_db, client = Database_connection().get_connection()
    productos_collection = Database_connection().get_collection("productos")
    consulta1 = Producto.get_producto(productos_collection,
                                      "electronics",
                                      100,
                                      200
                                      )
    consulta2 = Producto.get_product_type(productos_collection, "pocket")
    consulta3 = Producto.get_product_by_rate(productos_collection, 4)
    consulta4 = Producto.get_producto(productos_collection,
                                      "men's clothing",
                                      orden="rating.rate"
                                      )
    consulta5 = Producto.get_facturacion(productos_collection)
    consulta6 = Producto.get_facturacion(productos_collection, "category")
    context = {
        "consulta1": consulta1,
        "consulta2": consulta2,
        "consulta3": consulta3,
        "consulta4": consulta4,
        "consulta5": consulta5,
        "consulta6": consulta6
        }

    return HttpResponse(template.render(context, request))
