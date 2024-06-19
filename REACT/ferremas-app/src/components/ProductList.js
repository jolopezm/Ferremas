import React from 'react';
import Product from './Product';

export default function ProductList({ products, showInUSD, dollarRate }) {
  return (
    <div>
      <div className="basic-grid container-fluid">
        {products.length > 0 ? (
          products.map((product) => (
            <Product 
              key={product.id} 
              product={product} 
              showInUSD={showInUSD} 
              dollarRate={dollarRate} 
            />
          ))
        ) : (
          <p>No se encontraron productos.</p>
        )}
      </div>
    </div>
  );
}
