
import { BrowserRouter, Routes, Route } from "react-router-dom";
import { EventProvider } from "./context/EventContext";
import Navbar from "./components/Navbar";
import Events from "./pages/Events";
import Registrations from "./pages/Registrations";
import "./App.css";

function App() {
  return (
    <EventProvider>
      <BrowserRouter>
        <Navbar />

        <div className="container">
          <Routes>
            <Route path="/" element={<Events />} />
            <Route path="/registrations" element={<Registrations />} />
          </Routes>
        </div>
      </BrowserRouter>
    </EventProvider>
  );
}

export default App;
