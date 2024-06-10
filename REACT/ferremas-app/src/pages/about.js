import React, { useState, useEffect } from 'react';
import { useNavigate } from 'react-router-dom';
import Header from "../components/Header";
import Payment from "../components/Payment";
import { initTransaction } from '../API';

export default function About() {
  const [transactionData, setTransactionData] = useState(null);
  const [error, setError] = useState(null);
  const navigate = useNavigate();

  const handleInitTransaction = async () => {

    try {
      const data = {
        buy_order: String(Math.floor(Math.random() * 1000000)),
        session_id: String(Math.floor(Math.random() * 1000000)),
        amount: 20000,
        return_url: 'http:localhost:3000/asdad'
      };
      const responseData = await initTransaction(data);
      setTransactionData(responseData);
    } catch (error) {
      setError(error.message);
    }
  };

  return (
    <>
      <Header />
      <div className='container'>
        <div className='mb-3 mt-3'>
          <h1>About Page</h1>
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
      </div>
    </>
  );
}
