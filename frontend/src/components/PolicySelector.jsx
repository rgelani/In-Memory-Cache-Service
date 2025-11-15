import React from "react";

const POLICIES = [
  { value: "lru", label: "LRU" },
  { value: "lfu", label: "LFU" },
  { value: "arc", label: "ARC" },
  { value: "lru_ttl", label: "LRU + TTL" }
];

export default function PolicySelector({ policy, onChange }) {
  return (
    <div className="card" style={{ marginBottom: 16 }}>
      <div style={{ display: "flex", justifyContent: "space-between", alignItems: "center", gap: 12 }}>
        <div>
          <div className="card-title">Cache policy</div>
          <div style={{ fontSize: "0.8rem", color: "#9ca3af", marginTop: 4 }}>
            Switch between LRU, LFU, ARC and LRU+TTL to see how hit rate changes.
          </div>
        </div>
        <select
          className="select"
          value={policy}
          onChange={(e) => onChange(e.target.value)}
        >
          {POLICIES.map((p) => (
            <option key={p.value} value={p.value}>
              {p.label}
            </option>
          ))}
        </select>
      </div>
    </div>
  );
}
