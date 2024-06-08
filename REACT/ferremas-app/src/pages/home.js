import React, { useState, useEffect } from 'react';
import axios from 'axios';
import Header from "../components/Header";
import ProductCard from "../components/ProductCard";
import Filter from "../components/Filter";
import Footer from "../components/Footer"; // Import the Footer component

export default function Home() {
    const [products, setProducts] = useState([]);
    const [dollarRate, setDollarRate] = useState(null);
    const [showInUSD, setShowInUSD] = useState(false);
    const [categories, setCategories] = useState([]);
    const [selectedCategory, setSelectedCategory] = useState('');
    const [sortOrder, setSortOrder] = useState('');
    const [searchTerm, setSearchTerm] = useState('');

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

    useEffect(() => {
        const fetchCategories = async () => {
            try {
                const categoryResponse = await axios.get('http://localhost:8000/categorias/');
                setCategories(categoryResponse.data.categorias);
            } catch (error) {
                console.error('Error fetching categories:', error);
            }
        };

        fetchCategories();
    }, []);

    const handleShowInUSDChange = () => {
        setShowInUSD(!showInUSD);
    };

    const handleCategoryChange = (categoryId) => {
        setSelectedCategory(categoryId);
    };

    const handleSortChange = (order) => {
        setSortOrder(order);
    };

    const handleSearchChange = (event) => {
        setSearchTerm(event.target.value);
    };

    const filteredProducts = products
        .filter(product => 
            (!selectedCategory || product.categoria_id === parseInt(selectedCategory)) &&
            (!searchTerm || product.nombre.toLowerCase().includes(searchTerm.toLowerCase()))
        );

    const sortedProducts = filteredProducts.sort((a, b) => {
        if (sortOrder === 'price-asc') {
            return a.precio - b.precio;
        } else if (sortOrder === 'price-desc') {
            return b.precio - a.precio;
        }
        return 0;
    });

    return (
        <>
            <div className="container">
                <Header />
                <h1 className="text-center">Nuestro catálogo</h1>
                <form role="search" onSubmit={(e) => e.preventDefault()}>
                    <input 
                        name="search" 
                        type="search" 
                        placeholder="Search" 
                        value={searchTerm}
                        onChange={handleSearchChange}
                    />
                </form>
                <Filter
                    showInUSD={showInUSD}
                    onShowInUSDChange={handleShowInUSDChange}
                    categories={categories}
                    onCategoryChange={handleCategoryChange}
                    onSortChange={handleSortChange}
                />
                <div>
                    <div className="grid">
                        {sortedProducts.length > 0 ? (
                            sortedProducts.map((product) => (
                                <ProductCard 
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
                </div><br></br><hr></hr>
                <Footer /> {/* Add the Footer component */}
            </div>
        </>
    );
}
