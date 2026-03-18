const express = require('express');
const bodyParser = require('body-parser');
const cors = require('cors');
const fs = require('fs');
const path = require('path');
// Import our core Sentinel Services
const { analyzeCode } = require('./services/ai');
const { applySentinelPatch, notifyMergeRequest } = require('./services/gitlab');
require('dotenv').config();

const app = express();
app.use(cors());
app.use(bodyParser.json());

const PORT = process.env.PORT || 5000;

// Internal state for demo dashboard monitoring
let logs = [
  { id: 1, time: new Date().toLocaleTimeString(), action: 'System Initialized', detail: 'Sentinel AI Modules (Anthropic & GitLab) loaded', status: 'info' }
];
const addLog = (action, detail, status) => {
  logs.push({ id: logs.length + 1, time: new Date().toLocaleTimeString(), action, detail, status });
};

app.get('/api/logs', (req, res) => res.json(logs));

// Simulation Pipeline to showcase "The Vision" without waiting for a real GitLab MR
app.post('/api/simulate-scan', async (req, res) => {
  addLog('Scan Started', 'Simulated MR Diff received (Authentication module). Intercepting payload.', 'info');
  res.json({ message: 'Simulation initialized' });

  // 1. AI Analysis Phase
  setTimeout(() => {
    addLog('Claude 3.5 Analysis', 'Running Deep-Diff on intercepted code. Analyzing control flow and secrets...', 'process');
  }, 1500);

  setTimeout(() => {
    // We simulate Claude finding a critical bug
    addLog('Vulnerability Detected', 'CRITICAL (Secret Leak): Found exposed Stripe API key mapped to global config.', 'warning');
  }, 3500);

  // 2. Action/Remediation Phase
  setTimeout(() => {
    addLog('Zero-Touch Remediation', 'Drafting secure code replacement. Abstracting key to OpenBao vault variables.', 'process');
  }, 6000);

  // 3. GitLab Orchestration Phase (Simulated locally for demo)
  setTimeout(() => {
    addLog('Local Remediation', 'Rewriting payment_processor.js securely. Abstracting secret to ENV.', 'process');
    
    const filePath = path.join(__dirname, '..', 'vulnerable_app', 'payment_processor.js');
    const secureCode = `const STRIPE_SECRET_KEY = process.env.STRIPE_SECRET_KEY;\n\nfunction processPayment(amount) {\n  console.log('Using secure Environment Variable for transactions.');\n  // payment logic here\n}`;
    
    try {
      fs.writeFileSync(filePath, secureCode);
      addLog('File Updated', 'vulnerable_app/payment_processor.js patched successfully.', 'success');
    } catch (err) {
      addLog('Error', 'Failed to patch local file.', 'error');
    }
  }, 8500);

  setTimeout(() => {
    addLog('Pipeline Verification', 'Local build check passed. Remediation verified.', 'success');
  }, 11000);
});

// The Real Webhook (To be hooked up to GitLab later)
app.post('/webhook', async (req, res) => {
  const event = req.headers['x-gitlab-event'];
  if (event === 'Merge Request Hook') {
    addLog('Webhook Fired', `Project ${req.body.project.name} triggered MR analysis.`, 'info');
    // Here we will eventually extract the diff, call `analyzeCode()`, and trigger `applySentinelPatch()`
  }
  res.status(200).send('Event received');
});

app.listen(PORT, () => {
  console.log(`Sentinel Server running on http://localhost:${PORT}`);
});

