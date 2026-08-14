const express = require('express');
const cors = require('cors');
const bodyParser = require('body-parser');
const path = require('path');
const fs = require('fs');

const db = require('./src/db');
const authRoutes = require('./src/routes/auth');
const txRoutes = require('./src/routes/transactions');
const settingsRoutes = require('./src/routes/settings');
const trucksRoutes = require('./src/routes/trucks');

const app = express();
app.use(cors());
app.use(bodyParser.json());

app.use('/api/auth', authRoutes);
app.use('/api/transactions', txRoutes);
app.use('/api/settings', settingsRoutes);
app.use('/api/trucks', trucksRoutes);

app.get('/api/health', (req, res) => res.json({ status: 'ok' }));

const PORT = process.env.PORT || 4000;
app.listen(PORT, () => {
  console.log(`Backend listening on ${PORT}`);
});
