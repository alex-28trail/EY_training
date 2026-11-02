
import { Link } from "react-router-dom"
import "./BookingSuccess.css"

function BookingSuccess() {
  return (
    <main className="success-page">
      <div className="success-card">
        <div className="success-icon">✓</div>

        <h1>Booking Confirmed!</h1>

        <p>
          Your appointment has been saved successfully.
        </p>

        <p className="success-note">
          You can view your appointment in My Appointments.
        </p>

        <div className="success-actions">
          <Link to="/appointments" className="success-button">
            My Appointments
          </Link>

          <Link to="/providers" className="success-link">
            Book Another Appointment
          </Link>
        </div>
      </div>
    </main>
  )
}

export default BookingSuccess
