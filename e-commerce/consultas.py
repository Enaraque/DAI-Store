from Seed import connect_db
from rich import print

productos_collection, compras_collection = connect_db()

# Electrónica entre 100 y 200€, ordenados por precio
print("\n------------------------------------------------------------------")
print("[blue]1- Electrónica entre 100 y 200€, ordenados por precio[/blue]\n")
query = {"category": "electronics", "price": {"$gte": 100, "$lte": 200}}
orden = [("price", -1)]
resultado = productos_collection.find(query).sort(orden)

for p in resultado:
    print(p["title"], p["price"])

# Productos que contengan la palabra 'pocket' en la descripción
print("\n------------------------------------------------------------------")
print(
    "[blue]2- Productos que contengan la palabra 'pocket' en la "
    + "descripción[/blue]\n"
)
query = {"description": {"$regex": "pocket"}}
resultado = productos_collection.find(query)

for p in resultado:
    print(p["title"], p["description"])

# Productos con rating mayor que 4
print("\n------------------------------------------------------------------")
print("[blue]3- Productos con rating mayor que 4[/blue]\n")
query = {"rating.rate": {"$gt": 4}}
resultado = productos_collection.find(query)

for p in resultado:
    print(p["title"], p["rating"]["rate"])

# Ropa de hombre, ordenada por puntuación
print("\n------------------------------------------------------------------")
print("[blue]4- Ropa de hombre, ordenada por puntuación[/blue]\n")
query = {"category": "men's clothing"}
orden = [("rating.rate", 1)]
resultado = productos_collection.find(query).sort(orden)

for p in resultado:
    print(p["title"], p["rating"]["rate"])

# Facturación total
print("\n------------------------------------------------------------------")
print("[blue] 5- Facturación total[/blue]\n")
resultado = productos_collection.aggregate(
    [{"$group": {"_id": None, "total": {"$sum": "$price"}}}]
)
for r in resultado:
    print(f"Facturación total: {r['total']}")

# Facturación por categoría de producto
print("\n------------------------------------------------------------------")
print("[blue]6- Facturación por categoría de producto[/blue]\n")
resultado = productos_collection.aggregate(
    [
        {
            "$group": {"_id": "$category", "total": {"$sum": "$price"}},
        }
    ]
)

for r in resultado:
    print(r)
    # print(f"Facturación {r['_id']}: {r['total']}")
