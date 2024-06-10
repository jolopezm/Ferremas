import React from 'react';

export default function Footer() {
    return (
        <footer className="container-fluid">
            <div className="grid">
                <div>
                    <h3>Ferremas</h3>
                    <p>Proveedor lider en herramientas y materiales para construcción.</p>
                </div>
                <div>
                    <h3>Accesos rápidos</h3>
                    <ul>
                        <li><a href="#">Home</a></li>
                        <li><a href="#">Sobre nosotros</a></li>
                        <li><a href="#">Servicios</a></li>
                        <li><a href="#">Contacto</a></li>
                    </ul>
                </div>
                <div>
                    <h3>Contacto</h3>
                    <p>Email: info@ferremas.com</p>
                    <p>Teléfono: +56 9 12345678</p>
                    <p>Dirección: Antonio Varas 666, Providencia, Región Metropolitana</p>
                </div>
                <div>
                    <h3>Síganos</h3>
                    <ul className="social">
                        <li><a href="#">Facebook</a></li>
                        <li><a href="#">Twitter</a></li>
                        <li><a href="#">LinkedIn</a></li>
                        <li><a href="#">Instagram</a></li>
                    </ul>
                </div>
            </div>
            <div className="text-center">
                <p>&copy; {new Date().getFullYear()} Ferremas. Todos los derechos reservados.</p>
            </div>
        </footer>
    );
}
