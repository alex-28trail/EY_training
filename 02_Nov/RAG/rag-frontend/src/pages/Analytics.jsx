import { useEffect, useState } from "react";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer
} from "recharts";
import {
  Activity,
  CheckCircle,
  XCircle,
  Clock,
  Target,
  RefreshCw
} from "lucide-react";
import { getHistory } from "../services/api";
import "./Analytics.css";

function Analytics() {
  const [history, setHistory] = useState([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState("");

  const loadAnalytics = async () => {
    setLoading(true);
    setError("");

    try {
      const data = await getHistory();
      setHistory(data.history || []);
    } catch (error) {
      setError(
        error.response?.data?.detail ||
        "Unable to load analytics. Check whether FastAPI is running."
      );
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    loadAnalytics();
  }, []);

  const totalEvaluations = new Set(
    history.map((item) => item.evaluation_id)
  ).size;

  const successfulResponses = history.filter(
    (item) => item.status === "Success"
  ).length;

  const failedResponses = history.filter(
    (item) => item.status !== "Success"
  ).length;

  const averageResponseTime =
    history.length > 0
      ? history.reduce(
          (total, item) => total + Number(item.model_seconds || 0),
          0
        ) / history.length
      : 0;

  const ratedResponses = history.filter(
    (item) =>
      item.feedback === "Correct" ||
      item.feedback === "Incorrect"
  );

  const correctResponses = ratedResponses.filter(
    (item) => item.feedback === "Correct"
  ).length;

  const accuracy =
    ratedResponses.length > 0
      ? (correctResponses / ratedResponses.length) * 100
      : 0;

  const modelNames = [...new Set(
    history.map((item) => item.model_name)
  )];

  const modelPerformance = modelNames.map((modelName) => {
    const modelResults = history.filter(
      (item) => item.model_name === modelName
    );

    const averageTime =
      modelResults.reduce(
        (total, item) => total + Number(item.model_seconds || 0),
        0
      ) / modelResults.length;

    const modelRated = modelResults.filter(
      (item) =>
        item.feedback === "Correct" ||
        item.feedback === "Incorrect"
    );

    const modelCorrect = modelRated.filter(
      (item) => item.feedback === "Correct"
    ).length;

    const modelAccuracy =
      modelRated.length > 0
        ? (modelCorrect / modelRated.length) * 100
        : 0;

    return {
      name: modelName.replace("NVIDIA ", "").replace("Thinking Machines ", ""),
      averageTime: Number(averageTime.toFixed(2)),
      accuracy: Number(modelAccuracy.toFixed(1)),
      evaluations: modelResults.length
    };
  });

  const recentHistory = history.slice(0, 8);

  if (loading) {
    return (
      <div className="analytics-page">
        <div className="analytics-message">
          <div className="analytics-loader"></div>
          <p>Loading analytics...</p>
        </div>
      </div>
    );
  }

  return (
    <div className="analytics-page">
      <div className="analytics-heading">
        <div>
          <p className="analytics-eyebrow">PERFORMANCE OVERVIEW</p>
          <h1>Analytics</h1>
          <p>Track model performance and evaluation results.</p>
        </div>

        <button
          className="analytics-refresh"
          onClick={loadAnalytics}
          type="button"
        >
          <RefreshCw size={16} />
          Refresh
        </button>
      </div>

      {error && (
        <div className="analytics-error">
          {error}
        </div>
      )}

      {!error && history.length === 0 && (
        <div className="analytics-empty">
          <Activity size={30} />
          <h3>No analytics available</h3>
          <p>
            Run an evaluation in the Playground to see your results here.
          </p>
        </div>
      )}

      {history.length > 0 && (
        <>
          <div className="analytics-stats">
            <div className="analytics-stat-card">
              <div className="analytics-stat-icon purple">
                <Activity size={20} />
              </div>
              <p>Total Evaluations</p>
              <h2>{totalEvaluations}</h2>
            </div>

            <div className="analytics-stat-card">
              <div className="analytics-stat-icon green">
                <CheckCircle size={20} />
              </div>
              <p>Successful Responses</p>
              <h2>{successfulResponses}</h2>
            </div>

            <div className="analytics-stat-card">
              <div className="analytics-stat-icon red">
                <XCircle size={20} />
              </div>
              <p>Failed Responses</p>
              <h2>{failedResponses}</h2>
            </div>

            <div className="analytics-stat-card">
              <div className="analytics-stat-icon blue">
                <Clock size={20} />
              </div>
              <p>Average Response Time</p>
              <h2>{averageResponseTime.toFixed(2)}s</h2>
            </div>

            <div className="analytics-stat-card">
              <div className="analytics-stat-icon orange">
                <Target size={20} />
              </div>
              <p>Feedback Accuracy</p>
              <h2>
                {ratedResponses.length > 0
                  ? `${accuracy.toFixed(1)}%`
                  : "N/A"}
              </h2>
            </div>
          </div>

          <div className="analytics-chart-panel">
            <div className="analytics-panel-heading">
              <div>
                <h3>Model Response Time</h3>
                <p>Average response time for each AI model.</p>
              </div>
            </div>

            <div className="analytics-chart">
              <ResponsiveContainer width="100%" height="100%">
                <BarChart
                  data={modelPerformance}
                  margin={{
                    top: 15,
                    right: 15,
                    left: 0,
                    bottom: 10
                  }}
                >
                  <CartesianGrid
                    strokeDasharray="3 3"
                    stroke="#28344b"
                  />
                  <XAxis
                    dataKey="name"
                    stroke="#8994aa"
                    tick={{ fontSize: 11 }}
                  />
                  <YAxis
                    stroke="#8994aa"
                    tick={{ fontSize: 11 }}
                    unit="s"
                  />
                  <Tooltip
                    contentStyle={{
                      background: "#151f32",
                      border: "1px solid #34415a",
                      borderRadius: "8px",
                      color: "#ffffff"
                    }}
                  />
                  <Bar
                    dataKey="averageTime"
                    name="Average response time"
                    fill="#9274e8"
                    radius={[5, 5, 0, 0]}
                  />
                </BarChart>
              </ResponsiveContainer>
            </div>
          </div>

          <div className="analytics-table-panel">
            <div className="analytics-panel-heading">
              <div>
                <h3>Model Performance</h3>
                <p>Evaluation and feedback summary for each model.</p>
              </div>
            </div>

            <div className="analytics-table-wrapper">
              <table className="analytics-table">
                <thead>
                  <tr>
                    <th>Model</th>
                    <th>Evaluations</th>
                    <th>Avg. Response</th>
                    <th>Feedback Accuracy</th>
                  </tr>
                </thead>

                <tbody>
                  {modelPerformance.map((model) => (
                    <tr key={model.name}>
                      <td>{model.name}</td>
                      <td>{model.evaluations}</td>
                      <td>{model.averageTime}s</td>
                      <td>
                        {model.accuracy > 0
                          ? `${model.accuracy}%`
                          : "Not rated"}
                      </td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>

          <div className="analytics-table-panel">
            <div className="analytics-panel-heading">
              <div>
                <h3>Recent Evaluations</h3>
                <p>Your latest model responses.</p>
              </div>
            </div>

            <div className="analytics-table-wrapper">
              <table className="analytics-table">
                <thead>
                  <tr>
                    <th>Date</th>
                    <th>Model</th>
                    <th>Response Time</th>
                    <th>Status</th>
                    <th>Feedback</th>
                  </tr>
                </thead>

                <tbody>
                  {recentHistory.map((item, index) => (
                    <tr
                      key={`${item.evaluation_id}-${item.model_id}-${index}`}
                    >
                      <td>{item.timestamp}</td>
                      <td>{item.model_name}</td>
                      <td>{item.model_seconds}s</td>
                      <td>
                        <span
                          className={
                            item.status === "Success"
                              ? "analytics-status success"
                              : "analytics-status failed"
                          }
                        >
                          {item.status}
                        </span>
                      </td>
                      <td>{item.feedback}</td>
                    </tr>
                  ))}
                </tbody>
              </table>
            </div>
          </div>
        </>
      )}
    </div>
  );
}

export default Analytics;