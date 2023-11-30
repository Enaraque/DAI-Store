import sys
from django.db import models
from pydantic import BaseModel, FilePath, Field, EmailStr, validator
from typing import Any
from datetime import datetime
from utils import get_db_handle
from pymongo import MongoClient
from bson import ObjectId

sys.path.append("..")  # Adds higher directory to python modules path.


class Database_connection:
    db, client = get_db_handle("tienda", host="mongo", port=27017)

    @classmethod
    def get_connection(cls):
        return cls.db, cls.client

    @classmethod
    def get_collection(cls, collection_name):
        return cls.db[collection_name]


class Nota(BaseModel):
    rate: float = Field(ge=0.0, lt=5.0)
    count: int = Field(ge=1)


class Producto(BaseModel):
    _id: Any
    title: str
    price: float
    description: str
    category: str
    image: str | None
    rating: Nota

    # Validar que el nombre comience con mayúscula
    @validator("title")
    @classmethod
    def validate_nombre(cls, value):
        if not value[0].isupper():
            raise ValueError("El nombre debe comenzar con una letra mayúscula")
        return value

    @staticmethod
    def get_producto_by_id(collection, producto_id):
        return collection.find().skip(producto_id).limit(1)

    @staticmethod
    def get_productos_by_id_range(collection, min_id, max_id):
        return collection.find().skip(min_id).limit(min_id - (max_id+1))

    @staticmethod
    def get_producto(
        collection, category: str, min_price=0.0, max_price=float("inf"), orden="price"
    ):
        query = {"category": category, "price": {"$gte": min_price, "$lte": max_price}}
        orden = [(orden, -1)]

        return collection.find(query).sort(orden)

    @staticmethod
    def get_imagen_producto(collection, id: str):
        query = {"_id": id}
        return collection.find_one(query, {"_id": 0, "image": 1})

    @staticmethod
    def get_all_categories(collection):
        query = {"category": {"$exists": True}}
        return collection.find(query).distinct("category")

    @staticmethod
    def get_product_type(collection, type: str):
        query = {"description": {"$regex": type, "$options": "i"}}

        return collection.find(query)

    @staticmethod
    def get_product_by_rate(collection, min_rate=0.0, max_rate=float("inf")):
        query = {"rating.rate": {"$gt": min_rate, "$lt": max_rate}}

        return collection.find(query)

    @staticmethod
    def get_facturacion(collection, identificador=None):
        return collection.aggregate(
            [
                {
                    "$group": {
                        "_id": f"${identificador}",
                        "total": {"$sum": "$price"},
                    }
                },
                {
                    "$project": {
                        "categoria": "$_id",
                        "total_facturacion": "$total",
                    }
                },
            ]
        )

    @staticmethod
    def add_producto(collection, producto):
        producto = Producto(**producto)
        producto.rating = dict(producto.rating)  # type: ignore
        producto.image = None
        collection.insert_one(dict(producto))

    @staticmethod
    def delete_producto_by_id(collection, id: int):
        if documento := collection.find().skip(id).limit(1):
            id_del_documento = documento[0]["_id"]
            obj_id = ObjectId(id_del_documento)
            collection.delete_one({"_id": obj_id})

    @staticmethod
    def update_producto_by_id(collection, id: int, producto: dict):
        if documento := collection.find().skip(id).limit(1):
            id_del_documento = documento[0]["_id"]
            obj_id = ObjectId(id_del_documento)
            collection.update_one({"_id": obj_id}, {"$set": producto})

            return Producto.get_producto_by_id(collection, id)


class Compra(BaseModel):
    _id: Any
    usuario: EmailStr
    fecha: datetime
    productos: list
