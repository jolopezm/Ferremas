import React from 'react';

export default function ProductCard({ product, showInUSD, dollarRate }) {
    const getPriceInDollars = (price) => {
        if (showInUSD && dollarRate) {
            return (price / dollarRate).toFixed(2);
        }
        return price;
    };

    return (
        <article className="pico-background-azure-800 product-card">
            <div className="product-card">
                <img src={product.imagen_url} className="product-img" alt={product.nombre} />
                <div className="product-info">
                    <p className="product-name">{product.nombre}</p>
                    <div>{getPriceInDollars(product.precio)} {showInUSD ? 'USD' : 'CLP'}</div>
                    <div role='grid'>
                        <span className="text-muted summary-small"><p>{product.cantidad} disponibles</p></span>
                        <button className='btn-small'>
                            <div className='summary-small'>
                                Añadir al carro
                            </div>
                        </button>
                    </div>
                </div>
            </div>
        </article>
    );
}
