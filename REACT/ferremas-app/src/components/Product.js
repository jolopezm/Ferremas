import React from 'react';
import { useCart } from '../contexts/CartContext';
import { numberWithPoints } from '../API';

export default function Product({ product, showInUSD, dollarRate, onAdd, onRemove, isInCart }) {
  const { addToCart } = useCart();

  const handleAddToCart = () => {
    addToCart(product);
  };

  const getPriceInDollars = (price) => {
    if (showInUSD && dollarRate) {
      return (price / dollarRate * 1000).toFixed(2);
    }
    return price;
  };

  const handleIncrement = () => {
    if (onAdd) onAdd(product.id);
  };

  const handleDecrement = () => {
    if (onRemove) onRemove(product.id);
  };


  const defaultImageUrl = 'https://res.cloudinary.com/drsfnq5io/image/upload/v1719020941/img-productos-ferremas/image_gzb0wu.png';
  const productImageUrl = product.imagen_url || defaultImageUrl;
  const totalPrice = product.precio * product.quantity;

  return (
    <article className="product-card">
      <div>
        <img src={productImageUrl} className="product-img" alt="Imagen no disponible" />
        <div className="product-info">
          <p className="product-name">{product.nombre}</p>
          <div>{getPriceInDollars(numberWithPoints(product.precio))} {showInUSD ? 'USD' : 'CLP'}</div>
          <div role="grid">
            <span className="text-muted summary-small"><p>{product.cantidad} disponibles</p></span>
            {isInCart ? (
              <div>
                <div role="group" className="cuantificador">
                  <button className="btn-small" onClick={handleDecrement}>
                    -
                  </button>
                  <span>{product.quantity}</span>
                  <button className="btn-small" onClick={handleIncrement}>
                    +
                  </button>
                </div>
                <div>{numberWithPoints(totalPrice)} {showInUSD ? 'USD' : 'CLP'}</div>
              </div>
            ) : (
              <button className="btn-small" onClick={handleAddToCart}>
                <div className="summary-small">
                  Añadir al carro
                </div>
              </button>
            )}
          </div>
        </div>
      </div>
    </article>
  );
}
