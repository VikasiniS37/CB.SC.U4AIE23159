// const express = require("express");
// const app = express();

// // Middleware (IMPORTANT)
// app.use(express.json());

// // Basic route
// app.get("/", (req, res) => {
//   res.send("Backend server is running");
// });

// // Start server
// app.listen(3000, () => {
//   console.log("Server running on port 3000");
// });

const express = require("express");
const app = express();

app.use(express.json());

let items = [];

// ROOT (just to check server)
app.get("/", (req, res) => {
  res.send("Server running");
});

// ADD THIS (IMPORTANT)
app.get("/items", (req, res) => {
  res.json(items);
});

// ADD THIS
app.post("/items", (req, res) => {
  const item = req.body;
  items.push(item);
  res.json(item);
});
express.request().on("data", (chunk) => {
  console.log("Received chunk:", chunk.toString());
});     
app.listen(3000, () => {
  console.log("Server running on port 3000");
});
