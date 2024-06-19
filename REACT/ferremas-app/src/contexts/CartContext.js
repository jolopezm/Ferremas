// src/contexts/CartContext.js
import React, { createContext, useContext, useState, useEffect } from 'react';

const CartContext = createContext();

export const CartProvider = ({ children }) => {
  const [cart, setCart] = useState(() => {
    const savedCart = localStorage.getItem('cart');
    return savedCart ? JSON.parse(savedCart) : [];
  });

  useEffect(() => {
    localStorage.setItem('cart', JSON.stringify(cart));
  }, [cart]);

  const addToCart = (product) => {
    setCart((currentItems) => {
      const isItemFound = currentItems.find((item) => item.id === product.id);
      if (isItemFound) {
        return currentItems.map((item) => {
          if (item.id === product.id) {
            return { ...item, quantity: item.quantity + 1 };
          } else {
            return item;
          }
        });
      } else {
        return [...currentItems, { ...product, quantity: 1 }];
      }
    });
  };

  const removeItem = (id) => {
    setCart((currentItems) => {
      if (currentItems.find((item) => item.id === id)?.quantity === 1) {
        return currentItems.filter((item) => item.id !== id);
      } else {
        return currentItems.map((item) => {
          if (item.id === id) {
            return { ...item, quantity: item.quantity - 1 };
          } else {
            return item;
          }
        });
      }
    });
  };

  return (
    <CartContext.Provider value={{ cart, addToCart, removeItem }}>
      {children}
    </CartContext.Provider>
  );
};

export const useCart = () => {
  return useContext(CartContext);
};
