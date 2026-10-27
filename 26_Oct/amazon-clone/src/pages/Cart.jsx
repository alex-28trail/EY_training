
import { useNavigate } from "react-router-dom";

function Cart({ cart, removeFromCart }) {
  const navigate = useNavigate();

  const total = cart.reduce((sum, item) => sum + item.price, 0);

  return (
    <div className="container">
      <h1>Shopping Cart</h1>

      {cart.length === 0 ? (
        <p>Your cart is empty.</p>
      ) : (
        <>
          {cart.map((item, index) => (
            <div className="cart-item" key={index}>
              <span>{item.name} - ₹{item.price.toLocaleString("en-IN")}</span>

              <button onClick={() => removeFromCart(index)}>
                Remove
              </button>
            </div>
          ))}

          <h2>Total: ₹{total.toLocaleString("en-IN")}</h2>

          <button onClick={() => navigate("/login")}>
            Proceed to Payment
          </button>
        </>
      )}
    </div>
  );
}

export default Cart;
