
import { useNavigate } from "react-router-dom";

function Payment({ cart, setCart, setOrderPlaced }) {
  const navigate = useNavigate();

  const total = cart.reduce((sum, item) => sum + item.price, 0);

  const handlePayment = (e) => {
    e.preventDefault();

    if (cart.length === 0) {
      alert("Your cart is empty");
      navigate("/cart");
      return;
    }

    setOrderPlaced(true);
    setCart([]);
    navigate("/success");
  };

  return (
    <div className="form-box">
      <h2>Payment</h2>

      <h3>Total Amount: ₹{total.toLocaleString("en-IN")}</h3>

      <form onSubmit={handlePayment}>
        <label>Select Payment Method</label>

        <select required defaultValue="">
          <option value="" disabled>Select method</option>
          <option value="upi">UPI (Demo)</option>
          <option value="card">Card (Demo)</option>
          <option value="cod">Cash on Delivery (Demo)</option>
        </select>

        <button type="submit">
          Pay ₹{total.toLocaleString("en-IN")}
        </button>
      </form>

      <p className="note">Demo only - No real payment is processed.</p>
    </div>
  );
}

export default Payment;
