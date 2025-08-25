import React, { useState, useEffect } from "react";

function App() {
  const [ticker, setTicker] = useState("AAPL");
  const [result, setResult] = useState(null);
  const [loading, setLoading] = useState(false);

  // Example function that calls your FastAPI /update endpoint
  const fetchUpdate = async () => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/update", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          ticker: ticker
        })
      });
      const data = await res.json();
      setResult(data);
    } catch (err) {
      console.error("Error fetching data", err);
    } finally {
      setLoading(false);
    }
  };

  // Call FastAPI when page loads
  useEffect(() => {
    fetchUpdate();
  }, []);

  return (
    <div style={{ padding: "2rem", fontFamily: "sans-serif" }}>
      <h1>Agentic AI Stock Predictor</h1>

      <div style={{ marginBottom: "1rem" }}>
        <label>
          Stock Ticker:{" "}
          <input
            type="text"
            value={ticker}
            onChange={(e) => setTicker(e.target.value.toUpperCase())}
          />
        </label>
        <button onClick={fetchUpdate} style={{ marginLeft: "1rem" }}>
          Fetch
        </button>
      </div>

      {loading && <p>Loading...</p>}

      {result && (
        <div>
          <h2>Results</h2>
          <pre>{JSON.stringify(result, null, 2)}</pre>
        </div>
      )}
    </div>
  );
}

export default App;