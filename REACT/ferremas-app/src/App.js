// App.js
import React from "react";
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import { AuthProvider } from "./contexts/AuthContext";
import Home from './pages/Home';
import About from "./pages/About";
import Docs from "./pages/Docs";
import NotFound from "./pages/NotFound";
import Approved from "./components/Approved";
import Rejected from "./components/Rejected";
import Login from "./components/Login";
import ProtectedPage from "./components/Protected"

const App = () => {
  return (
    <div>
      <AuthProvider>
        <BrowserRouter>
          <Routes>
            <Route index element={<Home />} />
            <Route path='/home' element={<Home />} />
            <Route path='/about' element={<About />} />
            <Route path='/docs' element={<Docs />} /> 
            <Route path='/approved' element={<Approved />} />
            <Route path='/rejected' element={<Rejected />} />
            <Route path='*' element={<NotFound />} />
            <Route path='/login' element={<Login />} />
            <Route path='/protected' element={<ProtectedPage />} />
          </Routes>
        </BrowserRouter>
      </AuthProvider>
    </div>
  );
};

export default App;
