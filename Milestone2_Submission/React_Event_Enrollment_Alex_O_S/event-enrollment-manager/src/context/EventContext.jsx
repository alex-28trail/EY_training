
import {
  createContext,
  useContext,
  useState,
  useEffect
} from "react";

// Create Context
const EventContext = createContext();

// Initial Event Data
const initialEvents = [
  {
    id: "EV101",
    title: "Intro to Cloud Computing",
    category: "Technology",
    date: "10 Nov 2026",
    time: "10:00 AM",
    seats: 4
  },
  {
    id: "EV102",
    title: "Creative Writing Lab",
    category: "Arts",
    date: "12 Nov 2026",
    time: "2:00 PM",
    seats: 3
  },
  {
    id: "EV103",
    title: "Data Visualization Basics",
    category: "Technology",
    date: "14 Nov 2026",
    time: "11:00 AM",
    seats: 5
  },
  {
    id: "EV104",
    title: "Personal Finance Essentials",
    category: "Life Skills",
    date: "16 Nov 2026",
    time: "4:00 PM",
    seats: 4
  },
  {
    id: "EV105",
    title: "Public Speaking Practice",
    category: "Life Skills",
    date: "18 Nov 2026",
    time: "10:30 AM",
    seats: 3
  },
  {
    id: "EV106",
    title: "Digital Illustration Studio",
    category: "Arts",
    date: "20 Nov 2026",
    time: "1:00 PM",
    seats: 2
  }
];

// Event Provider
export function EventProvider({ children }) {

  // Load Events from LocalStorage
  const [events, setEvents] = useState(() => {
    const savedEvents = localStorage.getItem("events");

    return savedEvents
      ? JSON.parse(savedEvents)
      : initialEvents;
  });

  // Load Registrations from LocalStorage
  const [registrations, setRegistrations] = useState(() => {
    const savedRegistrations = localStorage.getItem("registrations");

    return savedRegistrations
      ? JSON.parse(savedRegistrations)
      : [];
  });

  // Save Events to LocalStorage
  useEffect(() => {
    localStorage.setItem("events", JSON.stringify(events));
  }, [events]);

  // Save Registrations to LocalStorage
  useEffect(() => {
    localStorage.setItem(
      "registrations",
      JSON.stringify(registrations)
    );
  }, [registrations]);

  // Register for Event
  const registerForEvent = (eventId, name, email) => {

    const selectedEvent = events.find(
      event => event.id === eventId
    );

    if (!selectedEvent || selectedEvent.seats <= 0) {
      return false;
    }

    const newRegistration = {
      id: Date.now(),
      eventId,
      name,
      email,
      eventTitle: selectedEvent.title
    };

    setRegistrations(prev => [
      ...prev,
      newRegistration
    ]);

    setEvents(prev =>
      prev.map(event =>
        event.id === eventId
          ? { ...event, seats: event.seats - 1 }
          : event
      )
    );

    return true;
  };

  // Cancel Registration
  const cancelRegistration = (registrationId) => {

    const registration = registrations.find(
      item => item.id === registrationId
    );

    if (!registration) {
      return false;
    }

    setRegistrations(prev =>
      prev.filter(item => item.id !== registrationId)
    );

    setEvents(prev =>
      prev.map(event =>
        event.id === registration.eventId
          ? { ...event, seats: event.seats + 1 }
          : event
      )
    );

    return true;
  };

  // Provide Data to Components
  return (
    <EventContext.Provider
      value={{
        events,
        setEvents,
        registrations,
        setRegistrations,
        registerForEvent,
        cancelRegistration
      }}
    >
      {children}
    </EventContext.Provider>
  );
}

// Custom Hook
export function useEvents() {
  return useContext(EventContext);
}
