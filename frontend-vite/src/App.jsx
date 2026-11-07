import { BrowserRouter, Routes, Route } from "react-router-dom";
import Home from "./pages/Home";
import Login from "./pages/Login";
import Signup from "./pages/Signup";
import Predict from "./pages/Predict";
import Models from "./pages/Models";
import Reviews from "./pages/Reviews";
import Dashboard from "./pages/Dashboard";
import About from "./pages/About";
import AboutDetails from "./pages/AboutDetails";

import { Toaster } from "react-hot-toast";


function App() {
  return (
    <BrowserRouter>
      <Toaster />
      <Routes>
        <Route path="/" element={<Home />} />
        <Route path="/login" element={<Login />} />
        <Route path="/signup" element={<Signup />} />
        <Route path="/predict" element={<Predict />} />
        <Route path="/models" element={<Models />} />
        <Route path="/reviews" element={<Reviews />} />
        <Route path="/dashboard" element={<Dashboard />} />
        <Route path="/about" element={<About />} />
        <Route path="/about/details" element={<AboutDetails />} />
      </Routes>
    </BrowserRouter>
  );
}

export default App;