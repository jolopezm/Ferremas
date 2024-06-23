import React, { useState, useEffect, useRef } from 'react';
import { useCart } from '../contexts/CartContext';
import { useNavigate, useLocation } from 'react-router-dom';
import { initTransaction, createTransaction, searchTransactionToken, numberWithPoints, createOrder, createOrderDetail, checkOrderCodeExists, commitTransaction } from '../API';
import Payment from "../components/Payment";
import Product from '../components/Product';
import cryptoRandomString from 'crypto-random-string';

export default function Carrito() {
  const { cart, addToCart, removeItem } = useCart();
  const [transactionData, setTransactionData] = useState(null);
  const [error, setError] = useState(null);
  const [orderCreated, setOrderCreated] = useState(null); // Estado para almacenar la orden creada
  const navigate = useNavigate();
  const location = useLocation();
  const codigo = useRef('');

  useEffect(() => {
    const verifyTransaction = async () => {
      const searchParams = new URLSearchParams(location.search);
      const tokenFromUrl = searchParams.get('token_ws');
      console.log('token: ', tokenFromUrl)
      const tbk_token = searchParams.get('TBK_TOKEN');
      const tbk_orden = searchParams.get('TBK_ORDEN_COMPRA');
      
      if (tokenFromUrl) {
        try {
          const response = await commitTransaction(tokenFromUrl);
          const response_code = response.data.response_code;
          console.log('Response code: ', response_code)

          if (response_code === 0) {
            navigate('/approved');
          } else {
            navigate('/rejected')
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

  useEffect(() => {
    codigo.current = generarCodigoAlfanumerico();
    console.log('Código:', codigo.current);
  }, [cart]);

  const generarCodigoAlfanumerico = (longitud = 8) => {
    return cryptoRandomString({ length: longitud, type: 'alphanumeric' });
  };

  const handleIncrement = (id) => {
    addToCart(cart.find(item => item.id === id));
  };

  const handleDecrement = (id) => {
    removeItem(id);
  };

  const calculateTotal = () => {
    return cart.reduce((total, item) => {
      return total + (item.precio * item.quantity);
    }, 0);
  };

  const createUniqueOrderCode = async () => {
    let code = generarCodigoAlfanumerico();
    while (await checkOrderCodeExists(code)) {
      code = generarCodigoAlfanumerico();
    }
    return code;
  };

  const handleCreateOrder = async () => {
    try {
      const orderCode = await createUniqueOrderCode();

      const orderData = {
        id: orderCode,
        fecha_compra: new Date().toISOString().split('T')[0],
        usuario_id: 1,
      };

      console.log('Order Data:', orderData);
      const createdOrder = await createOrder(orderData);

      for (const item of cart) {
        const orderDetailData = {
          orden_id: createdOrder.id,
          producto_id: item.id,
          cantidad: item.quantity,
        };

        console.log('Order Detail Data:', orderDetailData);

        await createOrderDetail(orderDetailData);
      }

      setOrderCreated(createdOrder); // Almacenar la orden creada en el estado

    } catch (error) {
      setError(error.message);
    }
  };

  const handleInitiateTransaction = async () => {
    try {


      const transactionData = {
        buy_order: String(Math.floor(Math.random() * 1000000)),
        session_id: String(Math.floor(Math.random() * 1000000)),
        amount: calculateTotal(),
        return_url: 'http://localhost:3000/carrito'
      };

      const responseData = await initTransaction(transactionData);
      setTransactionData(responseData);

    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <div className='container'>
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
            >
            </Product>
          ))
        ) : (
          <p>No hay productos en el carrito.</p>
        )}
      </div>

      {cart.length > 0 && (
        <div>
          <p>Total: ${numberWithPoints(calculateTotal())}</p>
          <button onClick={handleCreateOrder}>Crear Orden de Compra</button><br/><br/>
          <button onClick={handleInitiateTransaction}>Iniciar Transacción</button><br/><br/>
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
