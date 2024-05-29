import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Header from "../components/header";

export default function Home() {
  const [products, setProducts] = useState([]);
  const [cart, setCart] = useState([]); // State to manage cart items

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

  return (
    <>
      <Header />
      <div className='container'>
        <div className='mb-3 mt3'>
          <h1>Nuestro catalogo</h1>
          {products.length > 0 ? (
            <div className='row'>
              {products.map((product) => (
                <div className='col-md-4 mb-3' key={product.id}>
                  <div className="card" style={{ width: '18rem' }}>
                    {/*<img src="https://via.placeholder.com/150" className="card-img-top" alt="Imagen del producto" /> {/* Placeholder image */}
                    <div className="card-body">
                      <h5 className="card-title">{product.nombre}</h5>
                      <p className="card-text">
                        <b>Precio:</b> {product.precio} CLP <br />
                        <div className="d-flex align-items-center justify-content-between">
                          <button className="btn btn-dark" onClick={() => handleAddToCart(product)}>Agregar al carrito</button>
                          <span className="text-muted">{product.cantidad} disponibles</span>
                        </div>
                      </p>
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
