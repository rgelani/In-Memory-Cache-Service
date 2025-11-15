import React from "react";

export default function CacheStatsPanel({ stats }) {
  if (!stats) {
    return (
      <div className="card">
        <div className="card-title">Cache stats</div>
        <div style={{ marginTop: 8, fontSize: "0.9rem", color: "#9ca3af" }}>
          Waiting for data...
        </div>
      </div>
    );
  }

  const {
    capacity,
    current_size,
    hits,
    misses,
    evictions,
    hit_rate
  } = stats;

  const hitRatePercent = (hit_rate * 100).toFixed(1);

  return (
    <div className="grid" style={{ gridTemplateColumns: "repeat(4, minmax(0, 1fr))" }}>
      <div className="card">
        <div className="card-title">Hit rate</div>
        <div className="card-value">{hitRatePercent}%</div>
        <div style={{ marginTop: 6, fontSize: "0.8rem", color: "#9ca3af" }}>
          Higher is better. This is hits / (hits + misses).
        </div>
      </div>

      <div className="card">
        <div className="card-title">Size / Capacity</div>
        <div className="card-value">
          {current_size} / {capacity}
        </div>
        <div style={{ marginTop: 6, fontSize: "0.8rem", color: "#9ca3af" }}>
          How full your cache currently is.
        </div>
      </div>

      <div className="card">
        <div className="card-title">Hits / Misses</div>
        <div className="card-value">
          {hits} / {misses}
        </div>
        <div style={{ marginTop: 6, fontSize: "0.8rem", color: "#9ca3af" }}>
          Hits are served from memory. Misses go to the slow path.
        </div>
      </div>

      <div className="card">
        <div className="card-title">Evictions</div>
        <div className="card-value">{evictions}</div>
        <div style={{ marginTop: 6, fontSize: "0.8rem", color: "#9ca3af" }}>
          Keys removed when the cache ran out of space.
        </div>
      </div>
    </div>
  );
}
