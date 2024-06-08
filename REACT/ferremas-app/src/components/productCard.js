import React from 'react';

export default function ProductCard({ product, showInUSD, dollarRate }) {
    const getPriceInDollars = (price) => {
        if (showInUSD && dollarRate) {
            return (price / dollarRate).toFixed(2);
        }
        return price;
    };

    return (
        <article className="pico-background-azure-800">
            <div>
            <img src={product.imagen_url} class="product-img" alt={product.nombre} />
            </div>
            

            <p class="product-name">{product.nombre}</p>
            {getPriceInDollars(product.precio)} {showInUSD ? 'USD' : 'CLP'}
            <div role='grid'>
                <span className="text-muted">{product.cantidad} disponibles</span>
                <button className="btn btn-dark">Agregar al carrito</button>
            </div>
        </article>
    );
}
