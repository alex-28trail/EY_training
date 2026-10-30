
import { useState } from "react";
import { useEvents } from "../context/EventContext";
import EventCard from "../components/EventCard";

function Events() {
  const { events } = useEvents();

  const [search, setSearch] = useState("");
  const [category, setCategory] = useState("All");

  const filteredEvents = events.filter((event) => {
    const matchSearch = event.title
      .toLowerCase()
      .includes(search.toLowerCase());

    const matchCategory =
      category === "All" || event.category === category;

    return matchSearch && matchCategory;
  });

  return (
    <div className="events-page">
      <h2>Upcoming Events</h2>
      <p>Browse and register for upcoming events.</p>

      <div className="filters">
        <div className="search-box">
          <span className="search-icon">⌕</span>

          <input
            type="text"
            placeholder="Search events..."
            value={search}
            onChange={(e) => setSearch(e.target.value)}
          />

          {search && (
            <button
              className="clear-search"
              onClick={() => setSearch("")}
              type="button"
              aria-label="Clear search"
            >
              ×
            </button>
          )}
        </div>

        <select
          className="category-select"
          value={category}
          onChange={(e) => setCategory(e.target.value)}
        >
          <option value="All">All Categories</option>
          <option value="Technology">Technology</option>
          <option value="Arts">Arts</option>
          <option value="Life Skills">Life Skills</option>
        </select>
      </div>

      <p className="results-count">
        Showing {filteredEvents.length} of {events.length} events
      </p>

      <div className="event-list">
        {filteredEvents.length > 0 ? (
          filteredEvents.map((event) => (
            <EventCard key={event.id} event={event} />
          ))
        ) : (
          <p className="no-events">
            No events found. Try another search or category.
          </p>
        )}
      </div>
    </div>
  );
}

export default Events;
