
import { Routes, Route, Link, Navigate } from "react-router-dom";
import { useState } from "react";

import Home from "./pages/Home";
import Cart from "./pages/Cart";
import Login from "./pages/Login";
import Payment from "./pages/Payment.jsx";
import Success from "./pages/Success";
import NotFound from "./pages/NotFound";

function App() {
  const [cart, setCart] = useState([]);
  const [loggedIn, setLoggedIn] = useState(false);
  const [orderPlaced, setOrderPlaced] = useState(false);

  const addToCart = (product) => {
    setCart([...cart, product]);
  };

  const removeFromCart = (index) => {
    setCart(cart.filter((_, i) => i !== index));
  };

  return (
    <div>
      <header>
        <Link to="/" className="logo">amazon<span>.in</span></Link>

        <nav>
          <Link to="/">Home</Link>
          <Link to="/cart">Cart ({cart.length})</Link>
          <Link to="/login">{loggedIn ? "Account" : "Login"}</Link>
        </nav>
      </header>

      <Routes>
        <Route path="/" element={<Home addToCart={addToCart} />} />

        <Route
          path="/cart"
          element={<Cart cart={cart} removeFromCart={removeFromCart} />}
        />

        <Route
          path="/login"
          element={<Login setLoggedIn={setLoggedIn} />}
        />

        <Route
          path="/payment"
          element={
            loggedIn ? (
              <Payment
                cart={cart}
                setCart={setCart}
                setOrderPlaced={setOrderPlaced}
              />
            ) : (
              <Navigate to="/login" replace />
            )
          }
        />

        <Route
          path="/success"
          element={
            orderPlaced ? (
              <Success />
            ) : (
              <Navigate to="/" replace />
            )
          }
        />

        <Route path="*" element={<NotFound />} />
      </Routes>
    </div>
  );
}

export default App;
