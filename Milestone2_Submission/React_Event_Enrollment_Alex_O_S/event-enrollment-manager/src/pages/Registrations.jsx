
import { useEvents } from "../context/EventContext";

function Registrations() {
  const { registrations, cancelRegistration } = useEvents();

  const handleCancel = (registrationId) => {
    const confirmCancel = window.confirm(
      "Are you sure you want to cancel this registration?"
    );

    if (confirmCancel) {
      cancelRegistration(registrationId);
    }
  };

  return (
    <div className="registrations-page">
      <h2>My Registrations</h2>

      {registrations.length === 0 ? (
        <p>You haven't registered for any events yet.</p>
      ) : (
        <div className="registration-list">
          {registrations.map((registration) => (
            <div className="registration-card" key={registration.id}>
              <h3>{registration.eventTitle}</h3>

              <p>Event ID: {registration.eventId}</p>
              <p>Name: {registration.name}</p>
              <p>Email: {registration.email}</p>
              <p>Registration ID: {registration.id}</p>

              <button
                className="cancel-btn"
                onClick={() => handleCancel(registration.id)}
              >
                Cancel Registration
              </button>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}

export default Registrations;
