
import { useEffect, useState } from "react"
import { Link } from "react-router-dom"
import "./Providers.css"

const API_URL = "http://127.0.0.1:8000"

function Providers() {
  const [providers, setProviders] = useState([])
  const [loading, setLoading] = useState(true)
  const [error, setError] = useState("")

  useEffect(() => {
    async function fetchProviders() {
      try {
        const response = await fetch(`${API_URL}/providers`)

        if (!response.ok) {
          throw new Error("Unable to fetch providers")
        }

        const data = await response.json()
        setProviders(data)
      } catch (error) {
        setError(error.message)
      } finally {
        setLoading(false)
      }
    }

    fetchProviders()
  }, [])

  if (loading) {
    return <p>Loading providers...</p>
  }

  if (error) {
    return <p>Error: {error}</p>
  }

  return (
    <main className="providers-page">
      <h1>Our Service Providers</h1>

      <p className="providers-subtitle">
        Find a provider and choose a service that suits your needs.
      </p>

      {providers.length === 0 ? (
        <p>No providers are currently available.</p>
      ) : (
        <div className="providers-grid">
          {providers.map((provider) => (
            <div className="provider-card" key={provider.id}>
              <h2>{provider.name}</h2>

              <h3>{provider.specialty}</h3>

              <p>{provider.description}</p>

              <Link
                to={`/providers/${provider.id}/services`}
                className="provider-button"
              >
                View Services
              </Link>
            </div>
          ))}
        </div>
      )}
    </main>
  )
}

export default Providers
