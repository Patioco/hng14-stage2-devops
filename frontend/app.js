const express = require('express');
const axios = require('axios');
const path = require('path');

const app = express();

// Environment variable (important for Docker)
const API_URL = process.env.API_URL || "http://api:8000";

app.use(express.json());
app.use(express.static(path.join(__dirname, 'views')));

// Health endpoint
app.get('/health', (req, res) => {
  res.json({ status: "ok" });
});

// Submit job
app.post('/submit', async (req, res) => {
  try {
    const response = await axios.post(`${API_URL}/jobs`, {}, { timeout: 5000 });
    res.json(response.data);
  } catch (err) {
    console.error(err.message);
    res.status(500).json({ error: "failed to submit job" });
  }
});

// Check job status
app.get('/status/:id', async (req, res) => {
  try {
    const response = await axios.get(`${API_URL}/jobs/${req.params.id}`, { timeout: 5000 });
    res.json(response.data);
  } catch (err) {
    console.error(err.message);
    res.status(500).json({ error: "failed to fetch status" });
  }
});

// Start server
app.listen(3000, '0.0.0.0', () => {
  console.log('Frontend running on port 3000');
});