
import { useState } from "react"
import { Link } from "react-router-dom"
import "./Appointments.css"

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

function getToday() {
  const today = new Date()

  return [
    today.getFullYear(),
    String(today.getMonth() + 1).padStart(2, "0"),
    String(today.getDate()).padStart(2, "0")
  ].join("-")
}

function Appointments() {
  const [appointments, setAppointments] = useState(() => {
    return JSON.parse(localStorage.getItem("appointments") || "[]")
  })

  const [editingId, setEditingId] = useState(null)
  const [newDate, setNewDate] = useState("")
  const [newTime, setNewTime] = useState("")
  const [message, setMessage] = useState("")

  function cancelAppointment(id) {
    const confirmed = window.confirm(
      "Are you sure you want to cancel this appointment?"
    )

    if (!confirmed) {
      return
    }

    const updatedAppointments = appointments.map((appointment) =>
      appointment.id === id
        ? { ...appointment, status: "Cancelled" }
        : appointment
    )

    setAppointments(updatedAppointments)

    localStorage.setItem(
      "appointments",
      JSON.stringify(updatedAppointments)
    )

    setEditingId(null)
    setMessage("Appointment cancelled successfully.")
  }

  function startReschedule(appointment) {
    setEditingId(appointment.id)
    setNewDate(appointment.date)
    setNewTime(appointment.time)
    setMessage("")
  }

  function saveReschedule(appointment) {
    if (!newDate || !newTime) {
      setMessage("Please select both a date and a time.")
      return
    }

    if (newDate < getToday()) {
      setMessage("You cannot select a date in the past.")
      return
    }

    const conflictingAppointment = appointments.find(
      (item) =>
        item.id !== appointment.id &&
        item.providerName === appointment.providerName &&
        item.date === newDate &&
        item.time === newTime &&
        item.status !== "Cancelled"
    )

    if (conflictingAppointment) {
      setMessage(
        "This provider already has an appointment at that time. Please choose another slot."
      )
      return
    }

    const confirmed = window.confirm(
      `Reschedule your appointment to ${newDate} at ${newTime}?`
    )

    if (!confirmed) {
      return
    }

    const updatedAppointments = appointments.map((item) =>
      item.id === appointment.id
        ? {
            ...item,
            date: newDate,
            time: newTime
          }
        : item
    )

    setAppointments(updatedAppointments)

    localStorage.setItem(
      "appointments",
      JSON.stringify(updatedAppointments)
    )

    setEditingId(null)
    setMessage("Appointment rescheduled successfully.")
  }

  return (
    <main className="appointments-page">
      <h1>My Appointments</h1>

      <p className="appointments-subtitle">
        View and manage your scheduled appointments.
      </p>

      {message && (
        <p className="appointments-message" role="status">
          {message}
        </p>
      )}

      {appointments.length === 0 ? (
        <div className="empty-appointments">
          <h2>No Appointments Yet</h2>

          <p>
            You haven't booked any appointments. Explore our
            service providers to get started.
          </p>

          <Link to="/providers" className="appointments-button">
            Explore Providers
          </Link>
        </div>
      ) : (
        <div className="appointments-list">
          {appointments.map((appointment) => (
            <div className="appointment-card" key={appointment.id}>
              <div className="appointment-header">
                <h2>{appointment.serviceName}</h2>

                <span
                  className={`appointment-status ${appointment.status.toLowerCase()}`}
                >
                  {appointment.status}
                </span>
              </div>

              <p>
                <strong>Provider:</strong> {appointment.providerName}
              </p>

              <p>
                <strong>Patient:</strong> {appointment.customerName}
              </p>

              <p>
                <strong>Email:</strong> {appointment.customerEmail}
              </p>

              <p>
                <strong>Date:</strong> {appointment.date}
              </p>

              <p>
                <strong>Time:</strong> {appointment.time}
              </p>

              <p>
                <strong>Booking ID:</strong> {appointment.id}
              </p>

              {appointment.status !== "Cancelled" && (
                <>
                  {editingId === appointment.id ? (
                    <div className="reschedule-form">
                      <h3>Choose a New Schedule</h3>

                      <label htmlFor={`date-${appointment.id}`}>
                        New Date
                      </label>

                      <input
                        id={`date-${appointment.id}`}
                        type="date"
                        min={getToday()}
                        value={newDate}
                        onChange={(event) =>
                          setNewDate(event.target.value)
                        }
                        required
                      />

                      <label htmlFor={`time-${appointment.id}`}>
                        New Time
                      </label>

                      <select
                        id={`time-${appointment.id}`}
                        value={newTime}
                        onChange={(event) =>
                          setNewTime(event.target.value)
                        }
                        required
                      >
                        <option value="">Select a time</option>

                        {timeSlots.map((time) => (
                          <option key={time} value={time}>
                            {time}
                          </option>
                        ))}
                      </select>

                      <button
                        type="button"
                        className="reschedule-save"
                        onClick={() => saveReschedule(appointment)}
                      >
                        Confirm Reschedule
                      </button>

                      <button
                        type="button"
                        className="reschedule-cancel"
                        onClick={() => {
                          setEditingId(null)
                          setMessage("")
                        }}
                      >
                        Keep Original Appointment
                      </button>
                    </div>
                  ) : (
                    <button
                      type="button"
                      className="reschedule-button"
                      onClick={() => startReschedule(appointment)}
                    >
                      Reschedule
                    </button>
                  )}

                  <button
                    type="button"
                    className="cancel-button"
                    onClick={() => cancelAppointment(appointment.id)}
                  >
                    Cancel Appointment
                  </button>
                </>
              )}
            </div>
          ))}
        </div>
      )}

      <div className="appointments-footer">
        <Link to="/providers">Book Another Appointment</Link>
      </div>
    </main>
  )
}

export default Appointments
