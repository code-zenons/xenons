const express = require('express');
const rateLimit = require('express-rate-limit');

const app = express();
const port = 3000;

// Create a limiter that allows 100 requests per 15 minutes
const limiter = rateLimit({
	windowMs: 15 * 60 * 1000, // 15 minutes
	max: 100, // Limit each IP to 100 requests per `window` (here, per 15 minutes)
	standardHeaders: true, // Return rate limit info in the `RateLimit-*` headers
	legacyHeaders: false, // Disable the `X-RateLimit-*` headers
    message: 'Too many requests from this IP, please try again after 15 minutes',
});

// Apply the rate limiting middleware to all requests
app.use(limiter);

app.get('/', (req, res) => {
  res.send('Hello World! This server is protected directly from DoS attacks via rate limiting.');
});

app.get('/api/data', (req, res) => {
    res.json({ message: "This is some protected data.", timestamp: new Date() });
});

app.listen(port, () => {
  console.log(`Server listening on port ${port}`);
});
