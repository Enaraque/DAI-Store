# Proyecto DAI

En este repositorio se encuentra el código fuente del proyecto de la asignatura Desarrollo de Aplicaciones para Internet.

## Descripción

El proyecto consiste en una aplicación web de ecommerce. En ella podremos encontrar una serie de categorías de productos, cada una de ellas con una serie de productos. Cada producto tiene una serie de características, como el nombre, la descripción, el precio, etc. Además, cada producto tiene una serie de imágenes asociadas.

Podremos filtrar los productos por categorías así como por alguna palabra que contenga la descripción del producto. También podremos registrarnos en la aplicación, y una vez registrados, podremos crear nuevos productos y valorarlos.

Además disponemos de una API REST que nos permite obtener los productos que necesitemos, así como crear nuevos productos, modificarlos y eliminarlos.

Por último, la aplicación dispone de una parte de la práctica donde, junto con el servidor `Vite`, se ha desarrollado una aplicación de React que nos permite visualizar los productos de la aplicación donde, mediante el buscador podemos ir filtrando dinámicamente (por cada letra introducida mostramos los productos que aún coincidan) los productos que queremos ver.

## Tecnologías

Para el desarrollo de la aplicación se han utilizado las siguientes tecnologías:

- Python
- Django
- Ninja Extra
- HTML
- CSS
- Bootstrap
- JavaScript
- MongoDB

## Ejecución

La aplicación tiene diferentes modos de ejecución.

### Ejecución principal

En primer lugar, podremos ejecutar la aplicación principal ejecutada en el servidor de Django. Para ello, y ejecutaremos el siguiente comando:

```bash
docker compose up
```

Con esto ejecutaríamos la aplicación principal en el puerto 8000. Donde para acceder a ella, tendremos que ir a la dirección `http://0.0.0.0:8000/`.

### Ejecución de la aplicación de React

Si queremos ejecutar la aplicación de React, nos situaremos en la carpeta `isolate_practica5/front` y ejecutaremos el siguiente comando:

```bash
npx vite .
```

Una vez ejecutado, podremos acceder a la aplicación en la dirección `http://localhost:5173/`.

> [!IMPORTANT]
> Para que la aplicación funcione correctamente, es necesario que el servidor de Django esté ejecutándose, es decir, el docker debe estar levantado. Ya que nuestra aplicación de React hace uso de la API REST que proporciona el servidor de Django para obtener los productos.

### Despliegue

Para ejecutar la aplicacion en un entorno de producción, hemos hecho uso de `gunicorn` y `nginx`.
Este entorno de producción lo levantamos con el archivo `docker-compose.prod.yml`. Para ello, ejecutaremos el siguiente comando:

```bash
docker compose -f docker-compose.prod.yml up
```

Con esto ejecutaríamos la aplicación principal en el puerto 8088 con el que accederíamos al servidor de `nginx`. Donde para acceder a ella, tendremos que ir a la dirección `http://localhost:8088/etienda`.
