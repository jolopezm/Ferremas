// src/components/Header.js
import React, { useState } from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';
import { useCart } from '../contexts/CartContext';

export default function Header({ username }) {
  const { cart } = useCart();
  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();
  const [active, setActive] = useState(false);

  const quantity = cart.reduce((acc, curr) => {
    return acc + curr.quantity;
  }, 0);

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <div>
      <nav>
        <ul>
          <li>
            <img src="/imagenes/image.png" alt="Ferremas Logo" className="logo" />
          </li>
        </ul>
        <ul>
          <li><a href="http://localhost:3000/home">Home</a></li>
          <li><a href="http://localhost:3000/about">About</a></li>
          {isAuthenticated ? (
            <li>
              <details className='dropdown'>
                <summary className="summary-small"></summary>
                <ul className="dropdown-content summary-small">
                  <li><button onClick={handleLogout}>Logout</button></li>
                </ul>
              </details>
            </li>
          ) : (
            <li><a href="http://localhost:3000/login">Login</a></li>
          )}
          <li>
            <a href='/carrito' onClick={() => setActive(!active)}>
              <span className="bi--cart"></span>
              <span> {quantity}</span>
            </a>
          </li>
        </ul>
      </nav>
    </div>
  );
}
