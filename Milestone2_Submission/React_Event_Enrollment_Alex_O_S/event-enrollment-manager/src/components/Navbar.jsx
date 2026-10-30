
import { Link } from "react-router-dom";

function Navbar() {
  return (
    <nav className="navbar">
      <h2>Event Enrollment Manager</h2>

      <div className="nav-links">
        <Link to="/">Events</Link>
        <Link to="/registrations">Registrations</Link>
      </div>
    </nav>
  );
}

export default Navbar;
