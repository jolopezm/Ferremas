// App.js
import React from "react";
import { BrowserRouter, Routes, Route } from 'react-router-dom';
import Home from './pages/home';
import About from "./pages/about";
import Docs from "./pages/docs";
import NotFound from "./pages/notfound";
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
