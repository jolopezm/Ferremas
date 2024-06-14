import React from 'react';
import { useNavigate } from 'react-router-dom';
import { useAuth } from '../contexts/AuthContext';

export default function Header({ username }) {
  const { isAuthenticated, logout } = useAuth();
  const navigate = useNavigate();

  const handleLogout = () => {
    logout();
    navigate('/');
  };

  return (
    <div className="container">
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
                <summary className="summary-small">
                  <span className="simple-icons--user"></span>{username}
                </summary>
                <ul className="dropdown-content summary-small">
                  <li><a onClick={handleLogout}>Logout</a></li>
                </ul>
              </details>
            </li>
          ) : (
            <li><a href="http://localhost:3000/login">Login</a></li>
          )}
        </ul>
      </nav>
    </div>
  );
}
