import React from "react";
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from "./contexts/AuthContext";
import { CartProvider } from './contexts/CartContext';
import Home from './pages/Home';
import About from "./pages/About";
import Docs from "./pages/Docs";
import NotFound from "./pages/NotFound";
import Approved from "./components/Approved";
import Rejected from "./components/Rejected";
import Login from "./components/Login";
import ProtectedPage from "./components/Protected";
import Header from "./components/Header";
import Footer from "./components/Footer";
import Carrito from "./pages/Carrito";

const App = () => {
    return (
        <div className="container">
            <AuthProvider>
                <CartProvider>
                    <BrowserRouter>
                        <Header />
                        <Routes>
                            <Route index element={<Home />} />
                            <Route path='/home' element={<Home />} />
                            <Route path='/about' element={<About />} />
                            <Route path='/docs' element={<Docs />} />
                            <Route path='/approved' element={<Approved />} />
                            <Route path='/rejected' element={<Rejected />} />
                            <Route path='/login' element={<Login />} />
                            <Route path='/protected' element={<ProtectedPage />} />
                            <Route path='/carrito' element={<Carrito />} />
                            <Route path='*' element={<NotFound />} />
                        </Routes>
                        <Footer />
                    </BrowserRouter>
                </CartProvider>
            </AuthProvider>
        </div>
    );
};

export default App;
