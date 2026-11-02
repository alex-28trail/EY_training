
import { useEffect, useState } from "react"
import { Link, useParams } from "react-router-dom"
import "./Services.css"

const API_URL = "http://127.0.0.1:8000"

function Services() {
  const { providerId } = useParams()

  const [provider, setProvider] = useState(null)
  const [services, setServices] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  useEffect(() => {
    async function fetchServices() {
      try {
        const response = await fetch(
          `${API_URL}/providers/${providerId}/services`
        )

        if (!response.ok) {
          if (response.status === 404) {
            throw new Error("Provider not found")
          }

          throw new Error("Unable to fetch services")
        }

        const data = await response.json()

        setProvider(data.provider)
        setServices(data.services)
      } catch (error) {
        setError(error.message)
      } finally {
        setLoading(false)
      }
    }

    fetchServices()
  }, [providerId])

  if (loading) {
    return <p>Loading services...</p>
  }

  if (error) {
    return (
      <main className="services-page">
        <h1>{error}</h1>

        <Link to="/providers" className="service-button">
          Back to Providers
        </Link>
      </main>
    )
  }

  return (
    <main className="services-page">
      <Link to="/providers" className="back-link">
        &larr; Back to Providers
      </Link>

      <h1>Available Services</h1>

      <p className="services-subtitle">
        Services offered by {provider.name}
      </p>

      {services.length === 0 ? (
        <p>No services are currently available.</p>
      ) : (
        <div className="services-grid">
          {services.map((service) => (
            <div className="service-card" key={service.id}>
              <h2>{service.name}</h2>

              <p>{service.description}</p>

              <div className="service-details">
                <span>
                  {service.duration_minutes} minutes
                </span>

                <strong>
                  ₹{Number(service.price).toFixed(2)}
                </strong>
              </div>

              <Link
                to={`/booking/${service.id}`}
                className="service-button"
              >
                Book Appointment
              </Link>
            </div>
          ))}
        </div>
      )}
    </main>
  )
}

export default Services
