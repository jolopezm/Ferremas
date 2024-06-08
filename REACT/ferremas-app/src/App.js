// App.js
import React from "react";
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/Home';
import About from "./pages/About";
import Docs from "./pages/Docs";
import NotFound from "./pages/NotFound";
import Approved from "./components/Approved";
import Rejected from "./components/Rejected";

const App = () => {
  return (
    <div>
      <BrowserRouter>
        <Routes>
          <Route index element={<Home />} />
          <Route path='/home' element={<Home />} />
          <Route path='/about' element={<About />} />
          <Route path='/docs' element={<Docs />} />
          <Route path='/approved' element={<Approved />} />
          <Route path='/rejected' element={<Rejected />} />
          <Route path='*' element={<NotFound />} />
        </Routes>
      </BrowserRouter>
    </div>
  );
};

export default App;
