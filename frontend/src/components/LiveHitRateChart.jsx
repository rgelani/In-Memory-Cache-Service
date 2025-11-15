import React from "react";
import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer
} from "recharts";

export default function LiveHitRateChart({ history }) {
  const data = history.map((entry, index) => ({
    index,
    hitRate: +(entry.stats.hit_rate * 100).toFixed(2)
  }));

  return (
    <div className="card" style={{ marginTop: 16 }}>
      <div
        style={{
          display: "flex",
          justifyContent: "space-between",
          alignItems: "center",
          marginBottom: 12
        }}
      >
        <div>
          <div className="card-title">Hit rate over time</div>
          <div style={{ fontSize: "0.8rem", color: "#9ca3af", marginTop: 4 }}>
            Auto-refreshed every 2 seconds while the app is open.
          </div>
        </div>
        <span className="badge">
          Live
          <span
            style={{
              width: 6,
              height: 6,
              borderRadius: "9999px",
              backgroundColor: "#22c55e",
              marginLeft: 6
            }}
          />
        </span>
      </div>
      <div style={{ width: "100%", height: 240 }}>
        <ResponsiveContainer>
          <LineChart data={data}>
            <XAxis
              dataKey="index"
              tickFormatter={(v) => `${v * 2}s`}
              stroke="#6b7280"
            />
            <YAxis
              domain={[0, 100]}
              tickFormatter={(v) => `${v}%`}
              stroke="#6b7280"
            />
            <Tooltip
              formatter={(value) => `${value.toFixed(1)}%`}
              labelFormatter={(v) => `t = ${v * 2}s`}
            />
            <Line
              type="monotone"
              dataKey="hitRate"
              stroke="#6366f1"
              strokeWidth={2}
              dot={false}
            />
          </LineChart>
        </ResponsiveContainer>
      </div>
    </div>
  );
}
