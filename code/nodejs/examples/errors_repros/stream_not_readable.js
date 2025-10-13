const express = require('express');
const app = express();

app.use(express.json()); // This consumes the stream

app.post('/data', (req, res) => {
  let rawData = '';
  // *** THIS WILL LIKELY FAIL OR DO NOTHING ***
  // The stream was already read by express.json()
  req.on('data', (chunk) => {
    rawData += chunk;
  });
  req.on('end', () => {
    console.log('Raw data attempt:', rawData); // rawData will likely be empty
    console.log('Parsed body:', req.body); // Use this instead!
    res.json({ received: req.body });
  });
  req.on('error', (err) => {
     // You might hit an error here or just get no data
     console.error("Stream error:", err);
     // Potentially the "stream is not readable" error originates here
     // depending on timing and specific Node/Express versions.
  });
});

app.listen(3001, () => console.log('Server running on port 3001'));
