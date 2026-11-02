
import { Link, useNavigate } from "react-router-dom"
import { useAuth } from "../context/AuthContext"
import "./Navbar.css"

function Navbar() {
  const { user, isAuthenticated, logout } = useAuth()
  const navigate = useNavigate()

  function handleLogout() {
    logout()
    navigate("/login")
  }

  return (
    <nav className="navbar">
      <Link to="/" className="navbar-logo">
        AppointEase
      </Link>

      <div className="navbar-links">
        <Link to="/">Home</Link>
        <Link to="/providers">Providers</Link>
        <Link to="/appointments">My Appointments</Link>

        {isAuthenticated ? (
          <>
            <span className="navbar-user">
              Hi, {user?.name}
            </span>

            <button
              className="navbar-logout"
              onClick={handleLogout}
            >
              Logout
            </button>
          </>
        ) : (
          <>
            <Link to="/login">Login</Link>
            <Link to="/register">Register</Link>
          </>
        )}
      </div>
    </nav>
  )
}

export default Navbar
