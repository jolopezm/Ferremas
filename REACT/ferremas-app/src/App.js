import React, {useState, useEffect} from "react"
import api from './api'

const App = () => {
  const [productos, setProductos] = useState([]);
  const [formData, setFormData] = useState({
    nombre: '',
    precio: 0,
    cantidad: 0
  });

  const fetchProductos = async () => {
    try {
      const response = await api.get('/productos/');
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
    await api.post('/productos/', formData);
    fetchProductos();
    setFormData({
      nombre: '',
      precio: 0,
      cantidad: 0
    });
  };

  return (
    <div>

      <nav className="navbar navbar-dark bg-primary">
        <div className="container-fluid">
          <a className="navbar-brand" href="#">
            Ferremas
          </a>
        </div>
      </nav>

      <div className="container">
        <form onSubmit={handleFormSubmit}>
          <div className="mb-3 mt-3">
            <label htmlFor='nombre' className='form-label'>
              nombre
            </label>
            <input type='text' className="form-control" id='nombre' name='nombre' onChange={handleInputChange} value={formData.nombre}></input>
          </div>
        </form>
      </div>

      <div className="container">
        <form onSubmit={handleFormSubmit}>
          <div className="mb-3">
            <label htmlFor='precio' className='form-label'>
              precio
            </label>
            <input type='integer' className="form-control" id='precio' name='precio' onChange={handleInputChange} value={formData.precio}></input>
          </div>
        </form>
      </div>

      <div className="container">
        <form onSubmit={handleFormSubmit}>
          <div className="mb-3">
            <label htmlFor='cantidad' className='form-label'>
              cantidad
            </label>
            <input type='integer' className="form-control" id='cantidad' name='cantidad' onChange={handleInputChange} value={formData.cantidad}></input>
          </div>
        </form>
      </div>

      <div className="container">
      <button type='submit' className="btn btn-primary">
          submit
        </button>
      </div>

      <div className="container">
        <table className="table table-striped table-bordered table-hover">
        <thead>
          <tr>
            <th>nombre</th>
            <th>precio</th>
            <th>cantidad</th>
          </tr>
        </thead>
        <tbody>
          {productos.map((producto => (
            <tr key={producto.id}>
              <td>{producto.nombre}</td>
              <td>{producto.precio}</td>
              <td>{producto.cantidad}</td>
            </tr>
          )))}
        </tbody>
        </table>
      </div>
    </div>
  )
}

export default App;
