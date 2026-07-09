"use client";

import { motion } from "framer-motion";
import {
  Brain,
  Shield,
  Activity,
  Pill,
  Package,
  CheckCircle,
  AlertTriangle,
} from "lucide-react";

const agents = [
  {
    key: "predictor",
    icon: Brain,
    label: "Predictor",
    color: "#7c3aed",
    desc: "PyTorch MLP",
  },
  {
    key: "strategist",
    icon: Shield,
    label: "Strategist",
    color: "#06b6d4",
    desc: "Constraint Engine",
  },
  {
    key: "verifier",
    icon: Activity,
    label: "Verifier",
    color: "#3b82f6",
    desc: "CARD Neo4j",
  },
  {
    key: "pharmacist",
    icon: Pill,
    label: "Pharmacist",
    color: "#10b981",
    desc: "Formulary Check",
  },
  {
    key: "procurement",
    icon: Package,
    label: "Procurement",
    color: "#f59e0b",
    desc: "B2B Supply Chain",
  },
];

interface Props {
  result: any;
}

export default function AgentPipeline({ result }: Props) {
  const resistantCount = Object.values(result.ml_15_drug_profile || {}).filter(
    (d: any) => d.is_resistant,
  ).length;

  return (
    <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
      {/* Summary Cards */}
      <div
        style={{
          display: "grid",
          gridTemplateColumns: "repeat(3, 1fr)",
          gap: 12,
        }}
      >
        {[
          {
            label: "Selected Therapy",
            value: result.selected_therapy || "N/A",
            color: "#10b981",
            bg: "rgba(16,185,129,0.1)",
          },
          {
            label: "Resistant Drugs",
            value: `${resistantCount}/15`,
            color: "#ef4444",
            bg: "rgba(239,68,68,0.1)",
          },
          {
            label: "Stock Status",
            value: result.logistics_status?.status || "N/A",
            color: "#f59e0b",
            bg: "rgba(245,158,11,0.1)",
          },
        ].map((card) => (
          <motion.div
            key={card.label}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            className="glass"
            style={{ padding: 16 }}
          >
            <div
              style={{ fontSize: "0.7rem", color: "#64748b", marginBottom: 6 }}
            >
              {card.label}
            </div>
            <div
              style={{
                fontSize: "1rem",
                fontWeight: 700,
                color: card.color,
                background: card.bg,
                padding: "4px 10px",
                borderRadius: 6,
                display: "inline-block",
              }}
            >
              {card.value}
            </div>
          </motion.div>
        ))}
      </div>

      {/* Agent Pipeline */}
      <motion.div
        className="glass"
        style={{ padding: 24 }}
        initial={{ opacity: 0 }}
        animate={{ opacity: 1 }}
        transition={{ delay: 0.2 }}
      >
        <div
          style={{
            fontSize: "0.8rem",
            color: "#94a3b8",
            marginBottom: 20,
            fontWeight: 600,
          }}
        >
          AGENT PIPELINE EXECUTION
        </div>

        <div
          style={{
            display: "flex",
            alignItems: "center",
            gap: 8,
            flexWrap: "wrap",
          }}
        >
          {agents.map((agent, i) => (
            <div
              key={agent.key}
              style={{ display: "flex", alignItems: "center", gap: 8 }}
            >
              <motion.div
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ delay: i * 0.15 }}
                className="glass"
                style={{
                  padding: "12px 16px",
                  border: `1px solid ${agent.color}30`,
                  display: "flex",
                  alignItems: "center",
                  gap: 10,
                  position: "relative",
                  overflow: "hidden",
                }}
              >
                {/* Glow bg */}
                <div
                  style={{
                    position: "absolute",
                    inset: 0,
                    background: `radial-gradient(circle at 30% 50%, ${agent.color}10, transparent)`,
                    pointerEvents: "none",
                  }}
                />

                <div
                  style={{
                    width: 34,
                    height: 34,
                    background: `${agent.color}15`,
                    border: `1px solid ${agent.color}40`,
                    borderRadius: 8,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                    flexShrink: 0,
                  }}
                >
                  <agent.icon size={16} color={agent.color} />
                </div>

                <div>
                  <div
                    style={{
                      fontSize: "0.8rem",
                      fontWeight: 600,
                      color: "#f1f5f9",
                    }}
                  >
                    {agent.label}
                  </div>
                  <div style={{ fontSize: "0.65rem", color: "#64748b" }}>
                    {agent.desc}
                  </div>
                </div>

                <CheckCircle
                  size={14}
                  color="#10b981"
                  style={{ marginLeft: 4 }}
                />
              </motion.div>

              {i < agents.length - 1 && (
                <motion.div
                  initial={{ opacity: 0 }}
                  animate={{ opacity: [0.3, 1, 0.3] }}
                  transition={{
                    duration: 1.5,
                    repeat: Infinity,
                    delay: i * 0.2,
                  }}
                  style={{ color: "#475569" }}
                >
                  →
                </motion.div>
              )}
            </div>
          ))}
        </div>
      </motion.div>

      {/* Genomic Verification */}
      {result.genomic_verification?.length > 0 && (
        <motion.div
          className="glass"
          style={{ padding: 20 }}
          initial={{ opacity: 0, y: 10 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ delay: 0.4 }}
        >
          <div
            style={{
              fontSize: "0.8rem",
              color: "#94a3b8",
              marginBottom: 12,
              fontWeight: 600,
            }}
          >
            CARD GENOMIC EVIDENCE
          </div>
          {result.genomic_verification.map((gene: string, i: number) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, x: -10 }}
              animate={{ opacity: 1, x: 0 }}
              transition={{ delay: 0.5 + i * 0.1 }}
              style={{
                padding: "8px 12px",
                background: "rgba(59,130,246,0.08)",
                border: "1px solid rgba(59,130,246,0.2)",
                borderRadius: 8,
                fontSize: "0.78rem",
                color: "#94a3b8",
                marginBottom: 8,
                lineHeight: 1.5,
              }}
            >
              {gene}
            </motion.div>
          ))}
        </motion.div>
      )}

      {/* Audit Trace */}
      <motion.div
        className="glass"
        style={{ padding: 20 }}
        initial={{ opacity: 0, y: 10 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ delay: 0.5 }}
      >
        <div
          style={{
            fontSize: "0.8rem",
            color: "#94a3b8",
            marginBottom: 12,
            fontWeight: 600,
          }}
        >
          AUDIT TRACE
        </div>
        {result.trace?.map((log: string, i: number) => (
          <motion.div
            key={i}
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            transition={{ delay: 0.6 + i * 0.05 }}
            style={{
              fontSize: "0.75rem",
              color: "#64748b",
              padding: "4px 0",
              borderBottom: "1px solid rgba(255,255,255,0.03)",
              fontFamily: "monospace",
            }}
          >
            <span style={{ color: "#475569", marginRight: 8 }}>
              {String(i).padStart(2, "0")}
            </span>
            {log}
          </motion.div>
        ))}
      </motion.div>
    </div>
  );
}
