
import { useNavigate } from "react-router-dom";

function Success() {
  const navigate = useNavigate();

  return (
    <div className="success">
      <h1>✅ Order Placed Successfully!</h1>

      <p>Thank you for shopping with us.</p>

      <button onClick={() => navigate("/")}>
        Continue Shopping
      </button>
    </div>
  );
}

export default Success;
