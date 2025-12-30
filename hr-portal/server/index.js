const express = require('express');
const { spawn } = require('child_process');
const httpProxy = require('http-proxy');
const path = require('path');
const cors = require('cors');

const app = express();
const proxy = httpProxy.createProxyServer();

// Middleware
app.use(cors());
app.use(express.json());
app.use(express.urlencoded({ extended: true }));

// Start Streamlit landing page on port 8501
console.log('Starting Streamlit landing page...');
const streamlit = spawn('streamlit', ['run', '../app.py', '--server.port', '8501'], {
  cwd: __dirname
});

streamlit.stdout.on('data', (data) => {
  console.log(`Streamlit: ${data}`);
});

streamlit.stderr.on('data', (data) => {
  console.error(`Streamlit Error: ${data}`);
});

// API Routes
app.use('/api', require('./routes/api'));

// Serve React app for pass routes
app.use('/pass', express.static(path.join(__dirname, '../client/build')));
app.use('/admin', express.static(path.join(__dirname, '../client/build')));
app.use('/request', express.static(path.join(__dirname, '../client/build')));

// Proxy landing page to Streamlit
app.use('/', (req, res) => {
  proxy.web(req, res, { target: 'http://localhost:8501' });
});

// Handle proxy errors
proxy.on('error', (err, req, res) => {
  console.error('Proxy Error:', err);
  res.status(500).send('Proxy Error');
});

const PORT = process.env.PORT || 5000;
app.listen(PORT, () => {
  console.log(`
╔═══════════════════════════════════════════╗
║   BAYNUNAH HR PORTAL - SERVER RUNNING     ║
╚═══════════════════════════════════════════╝

🌐 Main Portal: http://localhost:${PORT}
📋 Employee Pass: http://localhost:${PORT}/pass/employee/:id
👔 Manager Pass: http://localhost:${PORT}/pass/manager/:id
📊 Admin Panel: http://localhost:${PORT}/admin
🔧 API: http://localhost:${PORT}/api

Status: ✅ Ready
  `);
});

// Graceful shutdown
process.on('SIGTERM', () => {
  console.log('SIGTERM received, shutting down gracefully...');
  streamlit.kill();
  process.exit(0);
});

process.on('SIGINT', () => {
  console.log('SIGINT received, shutting down gracefully...');
  streamlit.kill();
  process.exit(0);
});
