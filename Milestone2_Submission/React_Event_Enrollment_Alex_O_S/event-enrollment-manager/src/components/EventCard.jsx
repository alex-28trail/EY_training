
import { useState } from "react";
import { useEvents } from "../context/EventContext";

function EventCard({ event }) {
  const { registerForEvent } = useEvents();

  const [showForm, setShowForm] = useState(false);
  const [name, setName] = useState("");
  const [email, setEmail] = useState("");
  const [message, setMessage] = useState("");

  const handleRegister = (e) => {
    e.preventDefault();

    if (!name.trim() || !email.trim()) {
      setMessage("Please fill in all fields");
      return;
    }

    if (!/^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email)) {
      setMessage("Enter a valid email address");
      return;
    }

    const success = registerForEvent(event.id, name, email);

    if (success) {
      setMessage("Registration successful!");
      setName("");
      setEmail("");
      setShowForm(false);
    } else {
      setMessage("No seats available");
    }
  };

  return (
    <div className="event-card">
    <h3>{event.title}</h3>
    <p>Event ID: {event.id}</p>
    <p>{event.category}</p>
      <p>Date: {event.date}</p>
      <p>Time: {event.time}</p>
      <p>Available Seats: {event.seats}</p>

      {event.seats > 0 ? (
        <button onClick={() => setShowForm(!showForm)}>
          Register
        </button>
      ) : (
        <button disabled>Fully Booked</button>
      )}

      {showForm && (
        <form onSubmit={handleRegister} className="register-form">
          <input
            type="text"
            placeholder="Enter your name"
            value={name}
            onChange={(e) => setName(e.target.value)}
          />

          <input
            type="email"
            placeholder="Enter your email"
            value={email}
            onChange={(e) => setEmail(e.target.value)}
          />

          <button type="submit">Confirm Registration</button>
        </form>
      )}

      {message && <p>{message}</p>}
    </div>
  );
}

export default EventCard;
