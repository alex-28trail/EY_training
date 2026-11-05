
import { useEffect, useState } from "react";
import "./App.css";

const API = "http://127.0.0.1:8000";

function App() {
  const [activePage, setActivePage] = useState("dashboard");

  const [books, setBooks] = useState([]);
  const [reservations, setReservations] = useState([]);
  const [search, setSearch] = useState("");

  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const [selectedBook, setSelectedBook] = useState(null);
  const [customerName, setCustomerName] = useState("");
  const [reservationStep, setReservationStep] = useState("form");
  const [reservationMessage, setReservationMessage] = useState("");
  const [reservationLoading, setReservationLoading] = useState(false);

  const [chatMessages, setChatMessages] = useState([
    {
      role: "assistant",
      content:
        "Hello! I'm LibraAI, your library assistant. You can ask me to find books, check availability, or prepare a reservation."
    }
  ]);

  const [chatInput, setChatInput] = useState("");
  const [chatLoading, setChatLoading] = useState(false);
  const [pendingReservation, setPendingReservation] = useState(null);
  const [chatError, setChatError] = useState("");

  useEffect(() => {
    fetchBooks();
    fetchReservations();
  }, []);

  const fetchBooks = async () => {
    try {
      setLoading(true);
      setError("");

      const response = await fetch(`${API}/books`);

      if (!response.ok) {
        throw new Error("Unable to fetch books from the server.");
      }

      const data = await response.json();
      setBooks(data.books || []);
    } catch (err) {
      setError(err.message);
    } finally {
      setLoading(false);
    }
  };

  const fetchReservations = async () => {
    try {
      const response = await fetch(`${API}/reservations`);

      if (!response.ok) {
        throw new Error("Unable to fetch reservations.");
      }

      const data = await response.json();
      setReservations(data.reservations || []);
    } catch (err) {
      console.error(err);
    }
  };

  const filteredBooks = books.filter((book) => {
    const keyword = search.toLowerCase();

    return (
      book.title.toLowerCase().includes(keyword) ||
      book.author.toLowerCase().includes(keyword) ||
      book.category.toLowerCase().includes(keyword)
    );
  });

  const totalCopies = books.reduce(
    (total, book) => total + book.available_copies,
    0
  );

  const categories = new Set(books.map((book) => book.category));

  const getBookIcon = (category) => {
    const icons = {
      Programming: "🐍",
      "Artificial Intelligence": "🤖",
      "Machine Learning": "🧠",
      "Computer Science": "💻"
    };

    return icons[category] || "📚";
  };

  const openReservation = (book) => {
    setSelectedBook(book);
    setCustomerName("");
    setReservationStep("form");
    setReservationMessage("");
  };

  const closeReservation = () => {
    setSelectedBook(null);
    setCustomerName("");
    setReservationMessage("");
  };

  const previewReservation = async () => {
    if (!customerName.trim()) {
      setReservationMessage("Please enter your name.");
      return;
    }

    try {
      setReservationLoading(true);
      setReservationMessage("");

      const response = await fetch(`${API}/reservations/preview`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          book_id: selectedBook.id,
          customer_name: customerName.trim()
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Unable to check availability.");
      }

      setSelectedBook(data.book);
      setReservationStep("confirm");
    } catch (err) {
      setReservationMessage(err.message);
    } finally {
      setReservationLoading(false);
    }
  };

  const confirmReservation = async () => {
    try {
      setReservationLoading(true);
      setReservationMessage("");

      const response = await fetch(`${API}/reservations`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          book_id: selectedBook.id,
          customer_name: customerName.trim()
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Reservation failed.");
      }

      setReservationStep("success");
      setReservationMessage(
        `Reservation confirmed! Your reservation ID is ${data.reservation.reservation_id}.`
      );

      await fetchBooks();
      await fetchReservations();
    } catch (err) {
      setReservationMessage(err.message);
    } finally {
      setReservationLoading(false);
    }
  };

  const sendChatMessage = async (event) => {
    event.preventDefault();

    const question = chatInput.trim();

    if (!question || chatLoading) {
      return;
    }

    const updatedMessages = [
      ...chatMessages,
      { role: "user", content: question }
    ];

    setChatMessages(updatedMessages);
    setChatInput("");
    setChatLoading(true);
    setChatError("");
    setPendingReservation(null);

    try {
      const response = await fetch(`${API}/chat`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          messages: updatedMessages.map(({ role, content }) => ({
            role,
            content
          }))
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "The AI assistant could not respond.");
      }

      setChatMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content: data.reply
        }
      ]);

      setPendingReservation(data.pending_reservation || null);
    } catch (err) {
      setChatError(err.message);
    } finally {
      setChatLoading(false);
    }
  };

  const confirmAIReservation = async () => {
    if (!pendingReservation) return;

    try {
      setChatLoading(true);
      setChatError("");

      const response = await fetch(`${API}/reservations`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json"
        },
        body: JSON.stringify({
          book_id: pendingReservation.book.id,
          customer_name: pendingReservation.customer_name
        })
      });

      const data = await response.json();

      if (!response.ok) {
        throw new Error(data.detail || "Reservation could not be completed.");
      }

      setChatMessages((previous) => [
        ...previous,
        {
          role: "assistant",
          content:
            `Your reservation is confirmed! Your reservation ID is ${data.reservation.reservation_id}.`
        }
      ]);

      setPendingReservation(null);

      await fetchBooks();
      await fetchReservations();
    } catch (err) {
      setChatError(err.message);
    } finally {
      setChatLoading(false);
    }
  };

  const cancelAIReservation = () => {
    setPendingReservation(null);

    setChatMessages((previous) => [
      ...previous,
      {
        role: "assistant",
        content: "No problem. The reservation was cancelled and no changes were made."
      }
    ]);
  };

  const renderBooks = () => (
    <section className="books-section" id="books">
      <div className="section-heading">
        <div>
          <h2>Explore Books</h2>
          <p>Find something interesting to read.</p>
        </div>
        <span className="view-all">{filteredBooks.length} books</span>
      </div>

      <div className="search-bar">
        <span>🔍</span>
        <input
          type="text"
          placeholder="Search by book title, author or category..."
          value={search}
          onChange={(event) => setSearch(event.target.value)}
        />
      </div>

      {loading && <p>Loading books from the library...</p>}

      {error && (
        <div>
          <p style={{ color: "red" }}>{error}</p>
          <button onClick={fetchBooks}>Try Again</button>
        </div>
      )}

      {!loading && !error && (
        <div className="book-grid">
          {filteredBooks.length > 0 ? (
            filteredBooks.map((book) => (
              <div className="book-card" key={book.id}>
                <div className="book-cover">
                  <span>{getBookIcon(book.category)}</span>
                </div>

                <div className="book-info">
                  <span className="category">{book.category}</span>
                  <h3>{book.title}</h3>
                  <p>by {book.author}</p>

                  <div className="book-footer">
                    <span
                      className={
                        book.available_copies > 0
                          ? "available"
                          : "unavailable"
                      }
                    >
                      {book.available_copies > 0
                        ? `${book.available_copies} copies available`
                        : "Currently unavailable"}
                    </span>

                    <button
                      disabled={book.available_copies === 0}
                      onClick={() => openReservation(book)}
                    >
                      {book.available_copies > 0 ? "Reserve" : "Unavailable"}
                    </button>
                  </div>
                </div>
              </div>
            ))
          ) : (
            <p>No books found matching your search.</p>
          )}
        </div>
      )}
    </section>
  );

  const renderDashboard = () => (
    <>
      <section className="welcome-banner" id="dashboard">
        <div>
          <span className="eyebrow">YOUR SMART LIBRARY</span>
          <h1>Discover your next great read.</h1>
          <p>
            Search books, ask AI for recommendations, and reserve
            your favourite books effortlessly.
          </p>
          <button
            className="primary-button"
            onClick={() => {
              document.getElementById("books")?.scrollIntoView({
                behavior: "smooth"
              });
            }}
          >
            Explore Books →
          </button>
        </div>

        <div className="banner-icon">📚</div>
      </section>

      <section className="stats-grid">
        <div className="stat-card">
          <span>Total Books</span>
          <h2>{books.length}</h2>
          <small>In the library</small>
        </div>

        <div className="stat-card">
          <span>Available Copies</span>
          <h2>{totalCopies}</h2>
          <small>Ready to reserve</small>
        </div>

        <div className="stat-card">
          <span>Categories</span>
          <h2>{categories.size}</h2>
          <small>Explore different topics</small>
        </div>

        <div className="stat-card">
          <span>Reservations</span>
          <h2>{reservations.length}</h2>
          <small>Total reservations</small>
        </div>
      </section>

      {renderBooks()}

      <section className="assistant-banner">
        <div className="assistant-icon">🤖</div>
        <div>
          <h2>Meet your AI Library Assistant</h2>
          <p>
            Ask questions, find books, and prepare reservations using
            natural language.
          </p>
        </div>
        <button
          className="assistant-button"
          onClick={() => setActivePage("assistant")}
        >
          Start Chatting →
        </button>
      </section>
    </>
  );

  const renderReservations = () => (
    <section className="page-section">
      <div className="section-heading">
        <div>
          <h2>Reservation History</h2>
          <p>View all confirmed library reservations.</p>
        </div>
        <span className="view-all">
          {reservations.length} reservations
        </span>
      </div>

      <button
        className="refresh-button"
        onClick={fetchReservations}
      >
        ↻ Refresh
      </button>

      {reservations.length === 0 ? (
        <div className="empty-state">
          <span>📋</span>
          <h3>No reservations yet</h3>
          <p>Your confirmed reservations will appear here.</p>
        </div>
      ) : (
        <div className="reservation-list">
          {reservations.slice().reverse().map((item) => (
            <div
              className="reservation-card"
              key={item.reservation_id}
            >
              <div className="reservation-card-icon">📚</div>

              <div className="reservation-card-info">
                <h3>{item.book_title}</h3>
                <p>Reservation ID: {item.reservation_id}</p>
                <p>Customer: {item.customer_name}</p>
                <p>Date: {item.reservation_date}</p>
              </div>

              <span className="reservation-status">
                {item.status}
              </span>
            </div>
          ))}
        </div>
      )}
    </section>
  );

  const renderAssistant = () => (
    <section className="chat-page">
      <div className="chat-heading">
        <div className="chat-heading-icon">🤖</div>
        <div>
          <h2>LibraAI Assistant</h2>
          <p>Powered by OpenRouter · { " " }Ready to help</p>
        </div>
      </div>

      <div className="chat-messages">
        {chatMessages.map((message, index) => (
          <div
            key={index}
            className={`chat-message ${message.role === "user" ? "user-message" : "ai-message"}`}
          >
            <div className="chat-message-avatar">
              {message.role === "user" ? "A" : "🤖"}
            </div>
            <div className="chat-bubble">{message.content}</div>
          </div>
        ))}

        {chatLoading && (
          <div className="chat-message ai-message">
            <div className="chat-message-avatar">🤖</div>
            <div className="chat-bubble typing-indicator">
              LibraAI is thinking...
            </div>
          </div>
        )}
      </div>

      {pendingReservation && (
        <div className="ai-reservation-preview">
          <div>
            <span className="category">RESERVATION REQUEST</span>
            <h3>{pendingReservation.book.title}</h3>
            <p>Author: {pendingReservation.book.author}</p>
            <p>Customer: {pendingReservation.customer_name}</p>
            <p>
              Available copies: {pendingReservation.book.available_copies}
            </p>
            <p className="preview-warning">
              This reservation will only be saved after your confirmation.
            </p>
          </div>

          <div className="ai-reservation-actions">
            <button
              className="confirm-button"
              onClick={confirmAIReservation}
              disabled={chatLoading}
            >
              Confirm Reservation
            </button>
            <button
              className="cancel-button"
              onClick={cancelAIReservation}
              disabled={chatLoading}
            >
              Cancel
            </button>
          </div>
        </div>
      )}

      {chatError && <p className="chat-error">{chatError}</p>}

      <form className="chat-input-area" onSubmit={sendChatMessage}>
        <input
          type="text"
          placeholder="Ask LibraAI to find or reserve a book..."
          value={chatInput}
          onChange={(event) => setChatInput(event.target.value)}
          disabled={chatLoading}
        />
        <button type="submit" disabled={chatLoading || !chatInput.trim()}>
          Send ↑
        </button>
      </form>

      <p className="chat-hint">
        Example: "Find Python books" or "Reserve book 101 for Alex".
      </p>
    </section>
  );

  return (
    <div className="app">
      <aside className="sidebar">
        <div className="brand">
          <span className="brand-icon">📚</span>
          <span>LibraAI</span>
        </div>

        <p className="menu-label">MENU</p>

        <nav>
          <button
            className={`nav-item ${activePage === "dashboard" ? "active" : ""}`}
            onClick={() => setActivePage("dashboard")}
          >
            <span>▦</span> Dashboard
          </button>

          <button
            className={`nav-item ${activePage === "dashboard" ? "active" : ""}`}
            onClick={() => setActivePage("dashboard")}
          >
            <span>📖</span> Browse Books
          </button>

          <button
            className={`nav-item ${activePage === "assistant" ? "active" : ""}`}
            onClick={() => setActivePage("assistant")}
          >
            <span>🤖</span> AI Assistant
          </button>

          <button
            className={`nav-item ${activePage === "reservations" ? "active" : ""}`}
            onClick={() => setActivePage("reservations")}
          >
            <span>📋</span> Reservations
          </button>
        </nav>

        <div className="sidebar-bottom">
          <div className="profile">
            <div className="avatar">A</div>
            <div>
              <strong>Alex</strong>
              <small>Library Member</small>
            </div>
          </div>
        </div>
      </aside>

      <main className="main-content">
        <header className="topbar">
          <div>
            <h2>
              {activePage === "dashboard"
                ? "Library Dashboard"
                : activePage === "assistant"
                  ? "AI Library Assistant"
                  : "Reservations"}
            </h2>
            <p>Welcome back! Explore your library today.</p>
          </div>

          <div className="top-actions">
            <span className="notification">🔔</span>
            <div className="avatar">A</div>
          </div>
        </header>

        {activePage === "dashboard" && renderDashboard()}
        {activePage === "reservations" && renderReservations()}
        {activePage === "assistant" && renderAssistant()}
      </main>

      {selectedBook && (
        <div className="modal-overlay">
          <div className="reservation-modal">
            <button className="modal-close" onClick={closeReservation}>
              ×
            </button>

            {reservationStep === "form" && (
              <>
                <div className="modal-icon">📚</div>
                <h2>Reserve Your Book</h2>
                <p className="modal-description">
                  Enter your details to continue.
                </p>

                <div className="selected-book">
                  <strong>{selectedBook.title}</strong>
                  <small>by {selectedBook.author}</small>
                  <small>
                    {selectedBook.available_copies} copies available
                  </small>
                </div>

                <label htmlFor="customerName">Customer Name</label>
                <input
                  id="customerName"
                  type="text"
                  placeholder="Enter your full name"
                  value={customerName}
                  onChange={(event) => setCustomerName(event.target.value)}
                />

                {reservationMessage && (
                  <p className="modal-error">{reservationMessage}</p>
                )}

                <button
                  className="confirm-button"
                  onClick={previewReservation}
                  disabled={reservationLoading}
                >
                  {reservationLoading ? "Checking..." : "Continue"}
                </button>
              </>
            )}

            {reservationStep === "confirm" && (
              <>
                <div className="modal-icon">📝</div>
                <h2>Confirm Reservation</h2>
                <p className="modal-description">
                  Please review your reservation details.
                </p>

                <div className="selected-book">
                  <strong>{selectedBook.title}</strong>
                  <small>Author: {selectedBook.author}</small>
                  <small>Customer: {customerName}</small>
                  <small>
                    Available copies: {selectedBook.available_copies}
                  </small>
                </div>

                {reservationMessage && (
                  <p className="modal-error">{reservationMessage}</p>
                )}

                <button
                  className="confirm-button"
                  onClick={confirmReservation}
                  disabled={reservationLoading}
                >
                  {reservationLoading ? "Processing..." : "Confirm Reservation"}
                </button>

                <button
                  className="cancel-button"
                  onClick={() => {
                    setReservationStep("form");
                    setReservationMessage("");
                  }}
                  disabled={reservationLoading}
                >
                  Go Back
                </button>
              </>
            )}

            {reservationStep === "success" && (
              <>
                <div className="success-icon">✓</div>
                <h2>Reservation Successful!</h2>
                <p className="modal-description">
                  Your book has been reserved successfully.
                </p>

                <div className="success-message">
                  {reservationMessage}
                </div>

                <button className="confirm-button" onClick={closeReservation}>
                  Done
                </button>
              </>
            )}
          </div>
        </div>
      )}
    </div>
  );
}

export default App;
