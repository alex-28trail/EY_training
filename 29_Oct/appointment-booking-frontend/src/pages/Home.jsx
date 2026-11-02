import "./Home.css"
import { Link } from "react-router-dom"

function Home() {
  return (
    <main className="home-page">
      <section className="hero">
        <h1>Book Your Appointment Easily</h1>

        <p>
          Find the right service provider, choose an available
          time slot, and manage your appointments in one place.
        </p>

        <Link to="/providers" className="primary-button">
          Explore Providers
        </Link>
      </section>
    </main>
  )
}

export default Home
