import React, { useState, useEffect } from 'react';
import { useNavigate, useLocation } from 'react-router-dom';
import Header from "../components/Header";
import Payment from "../components/Payment";
import { initTransaction, createTransaction, searchTransactionToken } from '../API';

const About = () => {
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
              navigate('/rejected')
            }
        };

        verifyTransaction();
    }, [location.search, navigate]);

    const handleInitTransaction = async () => {
        try {
            const data = {
                buy_order: String(Math.floor(Math.random() * 1000000)),
                session_id: String(Math.floor(Math.random() * 1000000)),
                amount: 20000,
                return_url: 'http://localhost:3000/about'
            };
            const responseData = await initTransaction(data);
            setTransactionData(responseData);

            await createTransaction(responseData.token);

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
};

export default About;
