import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Header from "../components/header";

export default function Home() {
  const [products, setProducts] = useState([]);
  const [cart, setCart] = useState([]); // State to manage cart items
  const [dollarRate, setDollarRate] = useState(null); // State to store dollar rate
  const [showInUSD, setShowInUSD] = useState(false); // State to control showing prices in USD

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

  const handleAddToCart = (product) => {
    const existingCartItem = cart.find((item) => item.id === product.id);

    if (existingCartItem) {
      const updatedCart = cart.map((item) => {
        if (item.id === product.id) {
          return { ...item, quantity: item.quantity + 1 };
        }
        return item;
      });
      setCart(updatedCart);
    } else {
      setCart([...cart, { ...product, quantity: 1 }]);
    }
  };

  const getPriceInDollars = (price) => {
    if (showInUSD && dollarRate) {
      return (price / dollarRate).toFixed(2);
    }
    return price;
  };

  return (
    <>
  <Header />
  <div className='container d-flex flex-column align-items-center'>
    <div className='mb-3 mt-3 w-100' style={{ maxWidth: '600px' }}>
      <h1 className='text-center'>Nuestro catálogo</h1>
      <div className="form-check col-6" style={{ textAlign: 'left' }}>
        <input
          className="form-check-input"
          type="checkbox"
          id="showInUSDCheckbox"
          checked={showInUSD}
          onChange={() => setShowInUSD(!showInUSD)}
          style={{ maxWidth: '540px', border: '1px solid #000000' }}
        />
        <label className="form-check-label" htmlFor="showInUSDCheckbox">
          Mostrar en USD
        </label>
      </div>
      {products.length > 0 ? (
        <div className='row justify-content-center col-12'>
          {products.map((product) => (
            <div className='col-md-12 mb-3' key={product.id}>
              <div className="card mb-3" style={{ maxWidth: '540px', border: '1px solid #000000', borderRadius: '0px'}}>
                <div className="row g-0">

                  
                  <div className="col-md-4" style={{ border: '1px solid #000000' }}>
                    <img src={product.imagen_url} className="img-fluid rounded-start" alt={product.nombre} />
                  </div>
                  
                  <div className="col-md-8">
                    <div className="card-body">
                      <h5 className="card-title">{product.nombre}</h5>
                      <p className="card-text">
                        <b>Precio:</b> {getPriceInDollars(product.precio)} {showInUSD ? 'USD' : 'CLP'}
                      </p>
                      <div className="d-flex align-items-center justify-content-between">
                        <button className="btn btn-dark" onClick={() => handleAddToCart(product)}>Agregar al carrito</button>
                        <span className="text-muted">{product.cantidad} disponibles</span>
                      </div>
                    </div>
                  </div>
                </div>
              </div>
            </div>
          ))}
        </div>
      ) : (
        <p>Loading products...</p>
      )}
    </div>
  </div>
</>

  );
}
