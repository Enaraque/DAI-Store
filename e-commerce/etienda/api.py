from typing import Optional, List
from ninja_extra import NinjaExtraAPI, api_controller, http_get
from ninja import Schema, File
from .models import Database_connection as DB, Producto
from bson import ObjectId
import logging
from ninja.files import UploadedFile

logger = logging.getLogger(__name__)
api = NinjaExtraAPI()


class Rate(Schema):
    rate: float
    count: Optional[int]


class ProductSchema(Schema):  # sirve para validar y para documentación
    id: str
    title: str
    price: float
    description: str
    category: str
    image: str | None
    rating: Rate


class ProductSchemaIn(Schema):
    title: Optional[str]
    price: Optional[float]
    description: Optional[str]
    category: Optional[str]
    rating: Optional[Rate]


class ErrorSchema(Schema):
    message: str


def convertir_producto_id(producto):
    producto["id"] = str(producto["_id"])
    del producto["_id"]
    return producto


@api.get(
    "/productos",
    tags=["TIENDA DAI", "GETTERS"],
    response={202: List[ProductSchema], 404: ErrorSchema}
)
def get_productos_by_id_range(request, desde: int = 0, hasta: int = 4):
    productos_collection = DB.get_collection("productos")
    try:
        productos = Producto.get_productos_by_id_range(productos_collection, desde, hasta)
        productos_encontrados = [convertir_producto_id(producto) for producto in productos]
        return 202, productos_encontrados
    except Exception:
        return 404, {"message": "productos no encontrado"}


@api.post(
    "/productos",
    tags=["TIENDA DAI", "NEW"],
    response={202: ProductSchema, 404: ErrorSchema}
)
def add_producto(request, payload: ProductSchemaIn, imagen: UploadedFile = None):
    productos_collection = DB.get_collection("productos")
    try:
        producto = Producto.add_producto(productos_collection, payload.dict(), imagen)

        return 202, convertir_producto_id(producto[0])
    except Exception:
        return 404, {"message": "producto no encontrado"}


@api.get(
    "/productos/{producto_id}",
    tags=["TIENDA DAI", "GETTERS"],
    response={202: ProductSchema, 404: ErrorSchema}
)
def get_producto_by_id(request, producto_id: str):
    productos_collection = DB.get_collection("productos")
    try:
        producto = Producto.get_producto_by_id(productos_collection, producto_id)
        return 202, convertir_producto_id(producto)
    except Exception:
        return 404, {"message": "producto no encontrado"}


@api.delete(
    "/productos/{producto_id}",
    tags=["TIENDA DAI", "DELETE"],
    response={200: dict, 404: ErrorSchema}
)
def delete_producto_by_id(request, producto_id: str):
    productos_collection = DB.get_collection("productos")
    try:
        Producto.delete_producto_by_id(productos_collection, producto_id)
        return 200, {"message": "producto eliminado"}
    except Exception:
        return {"message": "producto no encontrado"}


@api.put(
    "/productos/{producto_id}",
    tags=["TIENDA DAI", "MODIFY"],
    response={202: ProductSchema, 404: ErrorSchema}
)
def modifica_producto(request, producto_id: str, payload: ProductSchemaIn):
    productos_collection = DB.get_collection("productos")
    try:
        payload_dict = {}

        for attr, value in payload.dict().items():
            if value is not None:
                payload_dict |= {attr: value}
        producto = Producto.update_producto_by_id(productos_collection, producto_id, payload_dict)

        return 202, convertir_producto_id(producto)
    except Exception:
        return 404, {"message": "producto no encontrado"}


@api.put(
    "/productos/{producto_id}/{rate}", tags=["TIENDA DAI", "MODIFY"],
    response={202: ProductSchema, 404: ErrorSchema}
)
def update_rating(request, producto_id: str, rate: float):
    productos_collection = DB.get_collection("productos")
    try:
        payload_dict = {"rating": {"rate": rate}}
        print("GERGERGERGERGERGERGERGERG\n\n\n\n\n")
        producto = Producto.update_producto_by_id(productos_collection, producto_id, payload_dict)
        return 202, convertir_producto_id(producto)

    except Exception:
        return 404, {"message": "producto no encontrado"}