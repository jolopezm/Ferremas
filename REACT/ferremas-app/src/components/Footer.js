import React from 'react';
import ThemeToggle from './ThemeToggle';

export default function Footer() {
    return (
        <footer>
            <br></br>
            <br></br>
            <hr></hr>
            <div className="grid">
                <div>
                    <h3>Ferremas</h3>
                    <p>Proveedor lider en herramientas y materiales para construcción.</p>
                    <ThemeToggle/>
                </div>
                <div>
                    <h3>Accesos rápidos</h3>
                    <ul>
                        <li><a href="/home">Home</a></li>
                        <li><a href="/about">Sobre nosotros</a></li>
                        <li><a href="/docs">Docs</a></li>
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
                        <li><a href="https://www.facebook.com/profile.php?id=61559656572650" target="_blank" rel="noopener noreferrer">Facebook</a></li>
                        <li><a href="https://x.com/FerremasHait" target="_blank" rel="noopener noreferrer">Twitter</a></li>
                        <li><a href="https://www.instagram.com/ferremashait/" target="_blank" rel="noopener noreferrer">Instagram</a></li>
                    </ul>
                </div>
            </div>
                <br></br>
                <br></br>
                <br></br>
                <br></br>
            <div className="text-center">
                <p>&copy; {new Date().getFullYear()} Ferremas. Todos los derechos reservados.</p><br></br>
            </div>
        </footer>
    );
}
