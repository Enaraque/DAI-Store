from pydantic import BaseModel, FilePath, Field, EmailStr
from pymongo import MongoClient
from pprint import pprint
from datetime import datetime
from typing import Any
import requests
import os


# https://requests.readthedocs.io/en/latest/
def getProductos(api):
    response = requests.get(api)
    return response.json()

# Esquema de la BD
# https://docs.pydantic.dev/latest/
# con anotaciones de tipo https://docs.python.org/3/library/typing.html
# https://docs.pydantic.dev/latest/usage/fields/


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


class Compra(BaseModel):
    _id: Any
    usuario: EmailStr
    fecha: datetime
    productos: list


def connect_db():
    client = MongoClient('mongo', 27017)
    tienda_db = client.tienda
    productos_collection = tienda_db.productos
    compras_collection = tienda_db.compras
    return productos_collection, compras_collection


def main():
    productos_collection, compras_collection = connect_db()

    productos = getProductos('https://fakestoreapi.com/products')
    for p in productos:
        respuesta = requests.get(p['image'])
        if respuesta.status_code == 200:
            dir_img = "img"
            if not os.path.exists(dir_img):
                os.makedirs(dir_img)

            nombre_archivo = os.path.join('img', os.path.basename(p['image']))
            with open(nombre_archivo, 'wb') as archivo:
                archivo.write(respuesta.content)

            p['image'] = os.path.basename(p['image'])
        else:
            p['image'] = False

        producto = Producto(**p)
        productos_collection.insert_one(producto.model_dump())


if __name__ == "__main__":
    main()
