import React, { useEffect, useState, useCallback } from "react";
import PolicySelector from "./components/PolicySelector";
import CacheStatsPanel from "./components/CacheStatsPanel";
import LiveHitRateChart from "./components/LiveHitRateChart";

const BACKEND_BASE_URL = "http://localhost:8000";

export default function App() {
  const [policy, setPolicy] = useState("lru");
  const [stats, setStats] = useState(null);
  const [history, setHistory] = useState([]);
  const [loadingDemo, setLoadingDemo] = useState(false);

  const fetchStats = useCallback(async () => {
    try {
      const res = await fetch(`${BACKEND_BASE_URL}/cache/${policy}/stats`);
      if (!res.ok) return;
      const data = await res.json();
      setStats(data.stats);
      setHistory((prev) => {
        const next = [...prev, { ts: Date.now(), stats: data.stats }];
        if (next.length > 60) next.shift();
        return next;
      });
    } catch (err) {
      // ignore for now or log to console
      console.error(err);
    }
  }, [policy]);

  useEffect(() => {
    setHistory([]);
    fetchStats();
    const interval = setInterval(fetchStats, 2000);
    return () => clearInterval(interval);
  }, [policy, fetchStats]);

  const triggerDemoTraffic = async () => {
    setLoadingDemo(true);
    try{
      await fetch(`${BACKEND_BASE_URL}/cache/${policy}/demo-traffic`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          reads: 200,
          writes: 40,
          key_space: 100
        })
      });
      await fetchStats();
    } catch (err) {
      console.error(err);
    } finally {
      setLoadingDemo(false);
    }
  };

  return (
    <div className="app-root">
      <div style={{ maxWidth: 1100, margin: "0 auto" }}>
        <header style={{ marginBottom: 24 }}>
          <div style={{ display: "flex", justifyContent: "space-between", gap: 16, alignItems: "center" }}>
            <div>
              <h1 style={{ fontSize: "1.6rem", margin: 0 }}>
                In-memory Cache Dashboard
              </h1>
              <p style={{ marginTop: 6, fontSize: "0.9rem", color: "#9ca3af" }}>
                Live stats for LRU, LFU, ARC and LRU+TTL policies backed by FastAPI.
              </p>
            </div>
            <button
              className="btn"
              onClick={triggerDemoTraffic}
              disabled={loadingDemo}
            >
              {loadingDemo ? "Generating traffic..." : "Generate demo traffic"}
            </button>
          </div>
        </header>

        <PolicySelector policy={policy} onChange={setPolicy} />
        <CacheStatsPanel stats={stats} />
        <LiveHitRateChart history={history} />

        <footer style={{ marginTop: 32, fontSize: "0.75rem", color: "#6b7280" }}>
          Tip: Open two browser tabs with this dashboard, hit the demo traffic button, and switch policies to see how hit rates behave.
        </footer>
      </div>
    </div>
  );
}
