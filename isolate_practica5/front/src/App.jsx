import React, { useState, useEffect } from 'react';
import reactLogo from './assets/react.svg'
import viteLogo from '/vite.svg'
import './App.css'
import Navegacion from "./componentes/Navegacion.jsx"
import Resultados from "./componentes/Resultados.jsx"


function App() {
  const [totalProductos, setProductos] = useState([]);
  const [productosFiltrados, setProductosFiltrados] = useState([]);

  /**
    * Realiza una solicitud para obtener los productos desde el servidor.
    * @returns {Promise<void>} Una promesa que se resuelve cuando se obtienen los productos correctamente.
    */
  useEffect(() => {
    const fetchData = async () => {
      try {
        const respuesta = await fetch('http://0.0.0.0:8000/etienda/api/productos?desde=0&hasta=100');
        const datosRecibidos = await respuesta.json();
        setProductos(datosRecibidos);
      } catch (error) {
        console.error('Error al obtener los productos:', error);
      }
    };

    fetchData();
  }, []);


  /**
    * Calcula el número total de categorías únicas a partir de un array de productos.
    * @param {Array} totalProductos - El array de productos.
    * @returns {Array} - Un array que contiene las categorías únicas.
    */
  const totalCategorias = (totalProductos) => {
    const categorias = totalProductos.map((producto) => producto.category);
    const categoriasUnicas = [...new Set(categorias)];
    return categoriasUnicas;
  }


  /**
   * Filtra los productos según el evento proporcionado.
   * @param {string | Event} evento - El evento que desencadena el filtrado. Puede ser una cadena de texto
   * si proviene de la lista de categorías, o un evento si proviene del buscador.
   */
  const filtrarProductos = (evento) => {
    // Si proviene de la lista de categorías
    if (typeof evento === 'string') {
      const productosFiltrados = totalProductos.filter((producto) => producto.category === evento);
      setProductosFiltrados(productosFiltrados);
    }
    // Si proviene del buscador (sabemos que es un evento)
    else {
      const valorActual = evento.target.value;
      const productosObtenidos = totalProductos.filter((producto) => producto.description.includes(valorActual));
      setProductosFiltrados(productosObtenidos);
    }
  }

  return (
    <>
      <Navegacion categorias={totalCategorias(totalProductos)} filtro={filtrarProductos} />
      <Resultados productos={productosFiltrados}/>
    </>
  );
}

export default App
