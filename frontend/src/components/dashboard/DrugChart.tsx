"use client";

import { motion } from "framer-motion";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  Cell,
} from "recharts";
import { Activity } from "lucide-react";

interface Props {
  drugs: Record<string, { is_resistant: boolean; confidence: number }>;
}

const CustomTooltip = ({ active, payload }: any) => {
  if (active && payload && payload.length) {
    const d = payload[0].payload;
    return (
      <div
        style={{
          background: "#12121f",
          border: "1px solid rgba(124,58,237,0.3)",
          borderRadius: 10,
          padding: "10px 14px",
          fontSize: "0.8rem",
        }}
      >
        <div style={{ color: "#f1f5f9", fontWeight: 600, marginBottom: 4 }}>
          {d.drug}
        </div>
        <div style={{ color: d.resistant ? "#ef4444" : "#10b981" }}>
          {d.resistant ? "⚠ Resistant" : "✓ Susceptible"}
        </div>
        <div style={{ color: "#94a3b8", marginTop: 2 }}>
          Confidence: {(d.confidence * 100).toFixed(1)}%
        </div>
      </div>
    );
  }
  return null;
};

export default function DrugChart({ drugs }: Props) {
  if (!drugs || Object.keys(drugs).length === 0) return null;

  const data = Object.entries(drugs)
    .map(([drug, val]) => ({
      drug,
      confidence: parseFloat((val.confidence * 100).toFixed(1)),
      resistant: val.is_resistant,
    }))
    .sort((a, b) => b.confidence - a.confidence);

  const resistantCount = data.filter((d) => d.resistant).length;
  const susceptibleCount = data.length - resistantCount;

  return (
    <motion.div
      className="glass"
      style={{ padding: 24 }}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ delay: 0.3 }}
    >
      {/* Header */}
      <div
        className="flex items-center justify-between"
        style={{ marginBottom: 20 }}
      >
        <div className="flex items-center gap-2">
          <Activity size={16} color="#7c3aed" />
          <span
            style={{ fontWeight: 700, fontSize: "0.9rem", color: "#f1f5f9" }}
          >
            15-Drug Resistance Profile
          </span>
        </div>
        <div className="flex gap-3">
          <span
            style={{
              fontSize: "0.72rem",
              fontWeight: 600,
              color: "#ef4444",
              background: "rgba(239,68,68,0.1)",
              padding: "3px 10px",
              borderRadius: 20,
            }}
          >
            {resistantCount} Resistant
          </span>
          <span
            style={{
              fontSize: "0.72rem",
              fontWeight: 600,
              color: "#10b981",
              background: "rgba(16,185,129,0.1)",
              padding: "3px 10px",
              borderRadius: 20,
            }}
          >
            {susceptibleCount} Susceptible
          </span>
        </div>
      </div>

      {/* Chart */}
      <ResponsiveContainer width="100%" height={280}>
        <BarChart
          data={data}
          margin={{ top: 5, right: 10, left: -20, bottom: 5 }}
        >
          <XAxis
            dataKey="drug"
            tick={{ fill: "#64748b", fontSize: 11 }}
            axisLine={false}
            tickLine={false}
          />
          <YAxis
            tick={{ fill: "#64748b", fontSize: 11 }}
            axisLine={false}
            tickLine={false}
            domain={[0, 100]}
            tickFormatter={(v) => `${v}%`}
          />
          <Tooltip
            content={<CustomTooltip />}
            cursor={{ fill: "rgba(124,58,237,0.05)" }}
          />
          <Bar dataKey="confidence" radius={[6, 6, 0, 0]}>
            {data.map((entry, i) => (
              <Cell
                key={i}
                fill={
                  entry.resistant
                    ? "url(#resistantGrad)"
                    : "url(#susceptibleGrad)"
                }
              />
            ))}
          </Bar>
          <defs>
            <linearGradient id="resistantGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#ef4444" stopOpacity={0.9} />
              <stop offset="100%" stopColor="#dc2626" stopOpacity={0.6} />
            </linearGradient>
            <linearGradient id="susceptibleGrad" x1="0" y1="0" x2="0" y2="1">
              <stop offset="0%" stopColor="#10b981" stopOpacity={0.9} />
              <stop offset="100%" stopColor="#059669" stopOpacity={0.6} />
            </linearGradient>
          </defs>
        </BarChart>
      </ResponsiveContainer>

      {/* Drug Tags */}
      <div
        style={{
          display: "flex",
          flexWrap: "wrap",
          gap: 8,
          marginTop: 16,
        }}
      >
        {data.map((d) => (
          <motion.div
            key={d.drug}
            whileHover={{ scale: 1.05 }}
            data-hover
            style={{
              padding: "4px 12px",
              borderRadius: 20,
              fontSize: "0.72rem",
              fontWeight: 600,
              background: d.resistant
                ? "rgba(239,68,68,0.1)"
                : "rgba(16,185,129,0.1)",
              border: `1px solid ${d.resistant ? "rgba(239,68,68,0.3)" : "rgba(16,185,129,0.3)"}`,
              color: d.resistant ? "#ef4444" : "#10b981",
              cursor: "none",
            }}
          >
            {d.drug} {d.resistant ? "✗" : "✓"}
          </motion.div>
        ))}
      </div>
    </motion.div>
  );
}
