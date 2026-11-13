import axios from 'axios';

// Vite proxies /api to http://localhost:8000 in vite.config.js
const API_BASE = '/api';

export const fetchTelemetry = async (segmentId = 0, channelId = 14, points = 80) => {
  const res = await axios.get(`${API_BASE}/telemetry/`, {
    params: { segment_id: segmentId, channel_id: channelId, points }
  });
  return res.data;
};

export const fetchDetection = async (segmentId = 0) => {
  const res = await axios.post(`${API_BASE}/detect/`, { segment_id: segmentId });
  return res.data;
};

export const fetchShapExplanation = async (segmentId = 0) => {
  const res = await axios.post(`${API_BASE}/detect/explain`, { segment_id: segmentId });
  return res.data;
};

export const fetchForecast = async (steps = 10, degrading = true) => {
  const res = await axios.get(`${API_BASE}/forecast/`, {
    params: { steps, degrading }
  });
  return res.data;
};

export const fetchAdvisory = async (segmentId, anomalyScore, shapSummary, topChannels, forecastWarning) => {
  const res = await axios.post(`${API_BASE}/advisory/`, {
    segment_id: segmentId,
    anomaly_score: anomalyScore,
    shap_summary: shapSummary,
    top_channels: topChannels,
    forecast_warning: forecastWarning
  });
  return res.data;
};

export const sendChatMessage = async (message) => {
  const res = await axios.post(`${API_BASE}/advisory/chat`, { message });
  return res.data;
};
