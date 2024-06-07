import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Header from "../components/header";
import ProductCard from "../components/productCard";
import ShowInUSD from "../components/ShowInUSD"; // Import ShowInUSD

export default function Home() {
    const [products, setProducts] = useState([]);
    const [dollarRate, setDollarRate] = useState(null);
    const [showInUSD, setShowInUSD] = useState(false);

    useEffect(() => {
        const fetchProducts = async () => {
            try {
                const productResponse = await axios.get('http://localhost:8000/productos/');
                setProducts(productResponse.data.productos);
            } catch (error) {
                console.error('Error fetching products:', error);
            }
        };

        fetchProducts();
    }, []);

    useEffect(() => {
        const fetchDollarRate = async () => {
            try {
                const response = await axios.get('http://localhost:8000/dollar-rate');
                setDollarRate(response.data.dollar_rate);
            } catch (error) {
                console.error('Error fetching dollar rate:', error);
            }
        };

        fetchDollarRate();
    }, []);

    const handleShowInUSDChange = () => {
        setShowInUSD(!showInUSD);
    };

    return (
        <>
            <div className='container'>
              <Header></Header>
                <ShowInUSD showInUSD={showInUSD} onShowInUSDChange={handleShowInUSDChange} />
                <div>
                    <h1 className='text-center'>Nuestro catálogo</h1>
                    <div className="grid">
                        {products.length > 0 ? (
                            products.map((product) => (
                                <ProductCard 
                                    key={product.id} 
                                    product={product} 
                                    showInUSD={showInUSD} 
                                    dollarRate={dollarRate} 
                                />
                            ))
                        ) : (
                            <p>Loading products...</p>
                        )}
                    </div>
                </div>
                <footer>soy un footer</footer>
            </div>
        </>
    );
}
