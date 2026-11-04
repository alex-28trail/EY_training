
import axios from "axios";

const API = axios.create({
  baseURL: "http://127.0.0.1:8000",
  headers: {
    "Content-Type": "application/json"
  }
});

export const evaluateQuestion = async (question) => {
  const response = await API.post("/api/evaluate", {
    question
  });

  return response.data;
};

export const submitFeedback = async (evaluationId, modelId, feedback) => {
  const response = await API.post("/api/feedback", {
    evaluation_id: evaluationId,
    model_id: modelId,
    feedback
  });

  return response.data;
};

export const getHistory = async () => {
  const response = await API.get("/api/history");
  return response.data;
};

export const getHealth = async () => {
  const response = await API.get("/api/health");
  return response.data;
};

export default API;
