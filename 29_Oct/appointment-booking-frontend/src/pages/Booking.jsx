
import { useState } from "react"
import { Link, useParams, useNavigate } from "react-router-dom"
import "./Booking.css"

const services = [
  {
    id: 1,
    providerId: 1,
    providerName: "Dr. John Mathew",
    name: "General Consultation",
    duration: "30 minutes",
    price: 500
  },
  {
    id: 2,
    providerId: 1,
    providerName: "Dr. John Mathew",
    name: "Follow-up Consultation",
    duration: "15 minutes",
    price: 300
  },
  {
    id: 3,
    providerId: 2,
    providerName: "Dr. Sarah Thomas",
    name: "Dental Checkup",
    duration: "30 minutes",
    price: 400
  },
  {
    id: 4,
    providerId: 2,
    providerName: "Dr. Sarah Thomas",
    name: "Teeth Cleaning",
    duration: "45 minutes",
    price: 800
  },
  {
    id: 5,
    providerId: 3,
    providerName: "Dr. Rahul Kumar",
    name: "Physiotherapy Session",
    duration: "45 minutes",
    price: 700
  },
  {
    id: 6,
    providerId: 3,
    providerName: "Dr. Rahul Kumar",
    name: "Pain Management",
    duration: "30 minutes",
    price: 600
  }
]

const timeSlots = [
  "09:00 AM",
  "09:30 AM",
  "10:00 AM",
  "10:30 AM",
  "11:00 AM",
  "11:30 AM",
  "12:00 PM",
  "02:00 PM",
  "02:30 PM",
  "03:00 PM",
  "03:30 PM",
  "04:00 PM"
]

function Booking() {
  const { serviceId } = useParams()
  const navigate = useNavigate()

  const service = services.find(
    (item) => item.id === Number(serviceId)
  )

  const [customerName, setCustomerName] = useState("")
  const [customerEmail, setCustomerEmail] = useState("")
  const [appointmentDate, setAppointmentDate] = useState("")
  const [selectedTime, setSelectedTime] = useState("")
  const [message, setMessage] = useState("")

  const today = new Date()
  const minDate = [
    today.getFullYear(),
    String(today.getMonth() + 1).padStart(2, "0"),
    String(today.getDate()).padStart(2, "0")
  ].join("-")

  function handleBooking(event) {
    event.preventDefault()

    if (!selectedTime) {
      setMessage("Please select an appointment time.")
      return
    }

    const booking = {
      id: Date.now(),
      customerName,
      customerEmail,
      serviceId: service.id,
      serviceName: service.name,
      providerName: service.providerName,
      date: appointmentDate,
      time: selectedTime,
      status: "Confirmed"
    }

    const existingBookings = JSON.parse(
      localStorage.getItem("appointments") || "[]"
    )

    existingBookings.push(booking)

    localStorage.setItem(
      "appointments",
      JSON.stringify(existingBookings)
    )

    navigate("/booking-success")
  }

  if (!service) {
    return (
      <main className="booking-page">
        <h1>Service Not Found</h1>
        <p>Please select a valid service before booking.</p>
        <Link to="/providers">Back to Providers</Link>
      </main>
    )
  }

  return (
    <main className="booking-page">
      <Link
        to={`/providers/${service.providerId}/services`}
        className="booking-back"
      >
        &larr; Back to Services
      </Link>

      <h1>Book Your Appointment</h1>

      <div className="booking-layout">
        <section className="booking-summary">
          <h2>Appointment Details</h2>

          <p>
            <strong>Provider:</strong> {service.providerName}
          </p>

          <p>
            <strong>Service:</strong> {service.name}
          </p>

          <p>
            <strong>Duration:</strong> {service.duration}
          </p>

          <p>
            <strong>Price:</strong> ₹{service.price}
          </p>
        </section>

        <form className="booking-form" onSubmit={handleBooking}>
          <h2>Your Details</h2>

          <label htmlFor="customerName">Full Name</label>
          <input
            id="customerName"
            type="text"
            value={customerName}
            onChange={(event) => setCustomerName(event.target.value)}
            required
            maxLength={100}
            placeholder="Enter your full name"
          />

          <label htmlFor="customerEmail">Email Address</label>
          <input
            id="customerEmail"
            type="email"
            value={customerEmail}
            onChange={(event) => setCustomerEmail(event.target.value)}
            required
            maxLength={254}
            placeholder="Enter your email"
          />

          <label htmlFor="appointmentDate">Appointment Date</label>
          <input
            id="appointmentDate"
            type="date"
            value={appointmentDate}
            min={minDate}
            onChange={(event) => {
              setAppointmentDate(event.target.value)
              setSelectedTime("")
            }}
            required
          />

          <label htmlFor="appointmentTime">Available Time Slots</label>
          <select
            id="appointmentTime"
            value={selectedTime}
            onChange={(event) => setSelectedTime(event.target.value)}
            required
          >
            <option value="">Select a time slot</option>

            {timeSlots.map((time) => (
              <option key={time} value={time}>
                {time}
              </option>
            ))}
          </select>

          {message && (
            <p className="booking-error">{message}</p>
          )}

          <button type="submit" className="booking-submit">
            Confirm Booking
          </button>
        </form>
      </div>
    </main>
  )
}

export default Booking
