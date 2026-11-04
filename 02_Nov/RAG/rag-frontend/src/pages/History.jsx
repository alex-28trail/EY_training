import { useEffect, useState } from "react";
import {
  Search,
  RefreshCw,
  Clock,
  FileText
} from "lucide-react";
import { getHistory } from "../services/api";
import "./History.css";

function History() {
  const [history, setHistory] = useState([]);
  const [search, setSearch] = useState("");
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadHistory = async () => {
    setLoading(true);
    setError("");

    try {
      const data = await getHistory();
      setHistory(data.history || []);
    } catch (error) {
      setError(
        error.response?.data?.detail ||
        "Unable to load evaluation history."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadHistory();
  }, []);

  const filteredHistory = history.filter((item) => {
    const searchText = search.toLowerCase();

    return (
      item.question?.toLowerCase().includes(searchText) ||
      item.model_name?.toLowerCase().includes(searchText) ||
      item.answer?.toLowerCase().includes(searchText)
    );
  });

  return (
    <div className="history-page">
      <div className="history-heading">
        <div>
          <p className="history-eyebrow">SAVED RECORDS</p>
          <h1>Evaluation History</h1>
          <p>View and search your previous model evaluations.</p>
        </div>

        <button
          className="history-refresh"
          onClick={loadHistory}
          type="button"
        >
          <RefreshCw size={16} />
          Refresh
        </button>
      </div>

      <div className="history-summary">
        <div className="history-summary-icon">
          <FileText size={22} />
        </div>

        <div>
          <p>Total model responses</p>
          <h2>{history.length}</h2>
        </div>

        <div className="history-summary-divider"></div>

        <div>
          <p>Unique evaluations</p>
          <h2>
            {new Set(history.map((item) => item.evaluation_id)).size}
          </h2>
        </div>
      </div>

      <div className="history-content">
        <div className="history-toolbar">
          <div>
            <h3>All Evaluations</h3>
            <p>{filteredHistory.length} records found</p>
          </div>

          <div className="history-search">
            <Search size={17} />
            <input
              type="text"
              placeholder="Search questions or models..."
              value={search}
              onChange={(event) => setSearch(event.target.value)}
            />
          </div>
        </div>

        {loading && (
          <div className="history-message">
            Loading evaluation history...
          </div>
        )}

        {error && (
          <div className="history-error">
            {error}
          </div>
        )}

        {!loading && !error && history.length === 0 && (
          <div className="history-message">
            <FileText size={30} />
            <h3>No evaluations found</h3>
            <p>Run an evaluation in Playground to create your first record.</p>
          </div>
        )}

        {!loading && !error && history.length > 0 && (
          <div className="history-table-wrapper">
            {filteredHistory.length === 0 ? (
              <div className="history-message">
                No matching records found.
              </div>
            ) : (
              <table className="history-table">
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Question</th>
                    <th>Model</th>
                    <th>Response Time</th>
                    <th>Status</th>
                    <th>Feedback</th>
                  </tr>
                </thead>

                <tbody>
                  {filteredHistory.map((item, index) => (
                    <tr
                      key={`${item.evaluation_id}-${item.model_id}-${index}`}
                    >
                      <td>{item.timestamp}</td>

                      <td className="history-question">
                        {item.question}
                      </td>

                      <td>{item.model_name}</td>

                      <td>
                        <span className="history-time">
                          <Clock size={13} />
                          {item.model_seconds}s
                        </span>
                      </td>

                      <td>
                        <span
                          className={`history-status ${
                            item.status === "Success"
                              ? "success"
                              : "failed"
                          }`}
                        >
                          {item.status}
                        </span>
                      </td>

                      <td>{item.feedback}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            )}
          </div>
        )}
      </div>
    </div>
  );
}

export default History;