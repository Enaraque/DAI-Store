import sys
from django.db import models
from pydantic import BaseModel, FilePath, Field, EmailStr, field_validator
from typing import Any
from datetime import datetime
from utils import get_db_handle
from pymongo import MongoClient
sys.path.append("..")  # Adds higher directory to python modules path.


class Database_connection:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super(Database_connection, cls).__new__(cls, *args,
                                                                    **kwargs)
        return cls._instance

    def __init__(self):
        if not hasattr(self, 'client'):
            self.db, self.client = get_db_handle('tienda', host='mongo',
                                                 port=27017
                                                 )

    def get_connection(self):
        return self.db, self.client

    def get_collection(self, collection_name):
        return self.db[collection_name]


class Nota(BaseModel):
    rate: float = Field(ge=0., lt=5.)
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
    @field_validator('title')
    @classmethod
    def validate_nombre(cls, value):
        if not value[0].isupper():
            raise ValueError("El nombre debe comenzar con una letra mayúscula")
        return value

    @staticmethod
    def get_producto(collection, category: str,
                     min_price=0.0, max_price=float('inf'), orden="price"):
        query = {"category": category,
                 "price": {"$gte": min_price,
                           "$lte": max_price
                           }
                 }
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
    def get_product_by_rate(collection, min_rate=0.0, max_rate=float('inf')):
        query = {"rating.rate": {"$gt": min_rate,
                                 "$lt": max_rate
                                 }
                 }

        return collection.find(query)

    @staticmethod
    def get_facturacion(collection, identificador=None):
        resultado = collection.aggregate([{"$group": {
                                                "_id": f"${identificador}",
                                                "total": {"$sum": "$price"}
                                                }
                                           },
                                          {"$project": {
                                                "categoria": "$_id",
                                                "total_facturacion": "$total",
                                                }
                                           }
                                          ]
                                         )
        return resultado

    @staticmethod
    def add_producto(collection, producto):
        producto = Producto(**producto)
        collection.insert_one(producto.model_dump())


class Compra(BaseModel):
    _id: Any
    usuario: EmailStr
    fecha: datetime
    productos: list
