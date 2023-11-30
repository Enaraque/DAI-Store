from typing import Optional
from ninja_extra import NinjaExtraAPI, api_controller, http_get
from ninja import Schema
from .models import Database_connection as DB, Producto
from bson import ObjectId
import logging
# from ninja.files import UploadedFile, File

logger = logging.getLogger(__name__)
api = NinjaExtraAPI()


class Rate(Schema):
    rate: float
    count: int


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


@api.get("/productos")
def get_productos_by_id_range(request, desde: int = 0, hasta: int = 4):
    productos_collection = DB.get_collection("productos")
    productos_encontrados = Producto.get_productos_by_id_range(productos_collection, desde, hasta)

    return [convertir_producto_id(producto) for producto in productos_encontrados]

# image: UploadedFile = File(...)
@api.post("/productos")
def add_producto(request, payload: ProductSchemaIn):
    productos_collection = DB.get_collection("productos")
    Producto.add_producto(productos_collection, payload.dict())
    return {"message": "producto agregado"}


@api.get("/productos/{producto_id}")
def get_producto_by_id(request, producto_id: int):
    productos_collection = DB.get_collection("productos")
    productos_encontrados = Producto.get_producto_by_id(
        productos_collection, producto_id
    )
    return [convertir_producto_id(producto) for producto in productos_encontrados]


@api.delete("/productos/{producto_id}")
def delete_producto_by_id(request, producto_id: int):
    productos_collection = DB.get_collection("productos")
    try:
        Producto.delete_producto_by_id(productos_collection, producto_id)
        return {"message": "producto eliminado"}
    except Exception:
        return {"message": "producto no encontrado"}


@api.put(
    "/productos/{producto_id}",
    tags=["TIENDA DAI"],
    response={202: ProductSchema, 404: ErrorSchema}
)
def modifica_producto(request, producto_id: int, payload: ProductSchemaIn):
    productos_collection = DB.get_collection("productos")
    try:
        payload_dict = {}

        for attr, value in payload.dict().items():
            if value is not None:
                payload_dict |= {attr: value}
        producto = Producto.update_producto_by_id(productos_collection, producto_id, payload_dict)

        return 202, convertir_producto_id(producto[0])
    except Exception:
        return 404, {"message": "producto no encontrado"}


# TODO:
# añadir mensajes de error
# producto puede ser modificado solo con los campos deseados, Para no modificar añadir None
