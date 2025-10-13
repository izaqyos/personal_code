require("dotenv").config({ path: `${__dirname}/.env` });
const PORT = process.env.PORT || 8000;
const cors = require("cors");
const express = require("express");
const app = express();

function requestLogger(req, res, next) {
  console.log(`--- Incoming Request ---`);
  console.log(`Method: ${req.method}`);
  console.log(`URL: ${req.url}`);
  console.log(`Headers:`);
  console.log(req.headers); // Object containing all request headers
  console.log(`Body:`);
  console.log(req.body); // Parsed request body (if applicable)
  console.log("--- End Request ---");

  next(); // Pass control to the next middleware or route handler
}

app.use(cors());
app.use(express.json());
app.use(requestLogger);

const { GoogleGenerativeAI } = require("@google/generative-ai");
const genAI = new GoogleGenerativeAI(process.env.API_KEY);

app.listen(PORT, () => console.log(`Listening on port ${PORT}.`));

app.post("/gemini", async (req, res) => {
  console.log(`Got request ${JSON.stringify(req.body)}.`);
  console.log(`history ${JSON.stringify(req.body.history)}.`);
  console.log(`message ${JSON.stringify(req.body.message)}.`);
  const model = genAI.getGenerativeModel({ model: "gemini-pro" });
  if (!model) {
    console.error("Failed to get generative model!");
    return;
  }
  const chat = model.startChat({
    parts: req.body.history,
    // message: req.body.message,
  });

  const msg = req.body.message;
  const response = await chat.sendMessage(msg);
  const resp = await response.response;
  const resp_text = resp.text();
  console.log(`Got response ${JSON.stringify(resp_text)}.`);
  res.send({status: 'ok', text: resp_text});
});

/* http get handler for /gemini - return model information */
app.get("/gemini", async (req, res) => {
  const model = genAI.getGenerativeModel({ model: "gemini-pro" });
  if (!model) {
    console.error("Failed to get generative model!");
    return;
  }
  const info = model.getInfo();
  res.send({status: 'ok', info: info});
})

