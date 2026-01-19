const axios = require('axios');

const TRICKLE_ENDPOINT = process.env.TRICKLE_ENDPOINT || '';
const TRICKLE_API_KEY = process.env.TRICKLE_API_KEY || '';

async function push(payload) {
  if (!TRICKLE_ENDPOINT) {
    throw new Error('TRICKLE_ENDPOINT is not configured in environment variables');
  }

  const headers = {
    'Content-Type': 'application/json'
  };

  if (TRICKLE_API_KEY) headers['Authorization'] = `Bearer ${TRICKLE_API_KEY}`;

  try {
    const resp = await axios.post(TRICKLE_ENDPOINT, payload, { headers });
    return { status: resp.status, data: resp.data };
  } catch (err) {
    // Bubble up a clearer error message
    const message = err.response && err.response.data ? JSON.stringify(err.response.data) : err.message;
    throw new Error(`Trickle push failed: ${message}`);
  }
}

module.exports = { push };
