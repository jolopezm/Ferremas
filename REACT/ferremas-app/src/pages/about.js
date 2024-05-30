import React, { useEffect } from 'react';
import Header from "../components/header";

export default function About() {
    // Obtener la imagen del producto desde el backend
    async function obtenerImagenProducto() {
        const productoId = 13; // ID del producto, ajustar según tu caso
        const url = `/productos/${productoId}/imagen`;

        try {
            const response = await fetch(url);
            const data = await response.json();

            if (response.ok) {
                const imagenUrl = data.imagen;

                // Crear un elemento <img> y establecer su atributo src
                const imagenElement = document.createElement("img");
                imagenElement.src = imagenUrl;

                // Agregar la imagen al contenedor en el HTML
                document.getElementById("imagen-producto").appendChild(imagenElement);
            } else {
                console.error(`Error: ${data.detail}`);
            }
        } catch (error) {
            console.error("Error al obtener la imagen del producto:", error);
        }
    }

    // Llamar a la función para obtener la imagen del producto al cargar la página
    useEffect(() => {
        obtenerImagenProducto();
    }, []); // Vacío para que se ejecute solo una vez al cargar el componente

    return (
        <>
            <Header />
            <div className='container'>
                <div className='mb-3 mt-3'>
                    <h1>about page</h1>
                </div>
                {/* Aquí se mostrará la imagen del producto */}
                <div id="imagen-producto"></div>
                <img src='https://res.cloudinary.com/drsfnq5io/image/upload/v1717044476/img-productos-ferremas/t0haehzve2ehdtvc9fw4.jpg'></img>
            </div>
        </>
    );
}
