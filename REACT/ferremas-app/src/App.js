import React, {useState, useEffect} from "react"
import api from './api'
import {BrowserRouter, Routes, Route} from 'react-router-dom';
import Home from './pages/home'
import About from "./pages/about";

const App = () => {
  const [productos, setProductos] = useState([]);
  const [formData, setFormData] = useState({
    nombre: '',
    precio: 0,
    cantidad: 0
  });

  const fetchProductos = async () => {
    try {
      const response = await api.get('/productos');
      if (response.status === 200) {
        setProductos(response.data);
      } else {
        throw new Error('Error al obtener los productos.');
      }
    } catch (error) {
      console.error('Error al obtener los productos:', error.message);
      // Aquí puedes manejar el error según tus necesidades (por ejemplo, mostrar un mensaje al usuario).
    }
  };
  

  useEffect(() => {
    fetchProductos();
  }, []);

  const handleInputChange = (event) => {
    const { name, value } = event.target;
    setFormData({
      ...formData,
      [name]: value,
    });
  };

  const handleFormSubmit = async (event) => {
    event.preventDefault();
    await api.post('/productos', formData);
    fetchProductos();
    setFormData({
      nombre: '',
      precio: 0,
      cantidad: 0
    });
  };

  return (
    <div>
      <BrowserRouter>
      <Routes>
        <Route index element={<Home></Home>}></Route>
        <Route path='/home' element={<Home></Home>}></Route>
        <Route path='/about' element={<About></About>}></Route>
      </Routes>
      </BrowserRouter>
    </div>
  )
}

export default App;
