// src/pages/Carrito.js
import React, { useState, useEffect } from 'react';
import { useCart } from '../contexts/CartContext';
import { useNavigate, useLocation } from 'react-router-dom';
import { initTransaction, createTransaction, searchTransactionToken, numberWithPoints } from '../API';
import Payment from "../components/Payment";
import Product from '../components/Product';

export default function Carrito() {
  const { cart, addToCart, removeItem } = useCart();
  const [transactionData, setTransactionData] = useState(null);
  const [error, setError] = useState(null);
  const navigate = useNavigate();
  const location = useLocation();

  useEffect(() => {
    const verifyTransaction = async () => {
      const searchParams = new URLSearchParams(location.search);
      const tokenFromUrl = searchParams.get('token_ws');
      const tbk_token = searchParams.get('TBK_TOKEN');
      const tbk_orden = searchParams.get('TBK_ORDEN_COMPRA');

      if (tokenFromUrl) {
        try {
          const transaction = await searchTransactionToken(tokenFromUrl);
          if (transaction) {
            navigate('/approved');
          }
        } catch (error) {
          setError(`Error al buscar transacción: ${error.message}`);
        }
      }
      if (tbk_orden && tbk_token) {
        navigate('/rejected');
      }
    };

    verifyTransaction();
  }, [location.search, navigate]);

  const handleIncrement = (id) => {
    addToCart(cart.find(item => item.id === id));
  };

  const handleDecrement = (id) => {
    removeItem(id);
  };

  // Calcular el total general de la orden
  const calculateTotal = () => {
    return cart.reduce((total, item) => {
      return total + (item.precio * item.quantity);
    }, 0);
  };

  const handleInitTransaction = async () => {
    try {
      const cart_amount = calculateTotal(); // Obtiene el total actualizado del carrito
      const data = {
        buy_order: String(Math.floor(Math.random() * 1000000)),
        session_id: String(Math.floor(Math.random() * 1000000)),
        amount: cart_amount,
        return_url: 'http://localhost:3000/carrito'
      };
      const responseData = await initTransaction(data);
      setTransactionData(responseData);

      await createTransaction(responseData.token);

    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <div>
      <h2>Carrito de Compras</h2>
      <div className="basic-grid container-fluid">
        {cart.length > 0 ? (
          cart.map((item) => (
            <Product 
              key={item.id} 
              product={item} 
              showInUSD={false} 
              dollarRate={null}
              onAdd={handleIncrement}
              onRemove={handleDecrement}
              isInCart={true}
            />
          ))
        ) : (
          <p>No hay productos en el carrito.</p>
        )}
      </div>

      {cart.length > 0 && (
        <div>
          <p>Total: ${numberWithPoints(calculateTotal())}</p>
          <button onClick={handleInitTransaction}>Iniciar Transacción</button>
          {transactionData && (
            <Payment
              url_tbk={transactionData.url}
              token={transactionData.token}
              submit="Continuar!"
            />
          )}
          {error && <div>Error: {error}</div>}
        </div>
      )}
    </div>
  );
}
