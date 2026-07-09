"use client";

import { motion } from "framer-motion";
import { useState } from "react";
import {
  Activity,
  Brain,
  Shield,
  Pill,
  Package,
  MessageSquare,
} from "lucide-react";
import Dashboard from "@/components/dashboard/Dashboard";

const agents = [
  { icon: Brain, label: "Predictor", color: "#7c3aed", desc: "PyTorch MLP" },
  {
    icon: Shield,
    label: "Strategist",
    color: "#06b6d4",
    desc: "Constraint Engine",
  },
  { icon: Activity, label: "Verifier", color: "#3b82f6", desc: "CARD Neo4j" },
  {
    icon: Pill,
    label: "Pharmacist",
    color: "#10b981",
    desc: "Formulary Check",
  },
  {
    icon: Package,
    label: "Procurement",
    color: "#f59e0b",
    desc: "B2B Supply Chain",
  },
];

export default function Home() {
  const [started, setStarted] = useState(false);

  if (started) return <Dashboard />;

  return (
    <main className="min-h-screen" style={{ background: "#0a0a0f" }}>
      {/* Header */}
      <motion.div
        initial={{ opacity: 0, y: -20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.6 }}
        className="flex items-center justify-between px-8 py-6"
        style={{ borderBottom: "1px solid rgba(124,58,237,0.15)" }}
      >
        <div className="flex items-center gap-3">
          <div
            style={{
              width: 36,
              height: 36,
              background: "linear-gradient(135deg, #7c3aed, #06b6d4)",
              borderRadius: 10,
              display: "flex",
              alignItems: "center",
              justifyContent: "center",
            }}
          >
            <Activity size={18} color="white" />
          </div>
          <span
            style={{ fontWeight: 700, fontSize: "1.1rem", color: "#f1f5f9" }}
          >
            Sentinel<span className="gradient-text">-CDS</span>
          </span>
        </div>
        <div
          style={{
            fontSize: "0.75rem",
            color: "#10b981",
            background: "rgba(16,185,129,0.1)",
            border: "1px solid rgba(16,185,129,0.2)",
            padding: "4px 12px",
            borderRadius: 20,
          }}
        >
          ● SYSTEM ONLINE
        </div>
      </motion.div>

      {/* Hero */}
      <div
        className="flex flex-col items-center justify-center text-center px-8"
        style={{ paddingTop: "8rem", paddingBottom: "4rem" }}
      >
        <motion.div
          initial={{ opacity: 0, scale: 0.9 }}
          animate={{ opacity: 1, scale: 1 }}
          transition={{ duration: 0.8, delay: 0.2 }}
        >
          <div
            style={{
              fontSize: "0.75rem",
              letterSpacing: "0.2em",
              color: "#7c3aed",
              marginBottom: "1.5rem",
              textTransform: "uppercase",
            }}
          >
            Autonomous Clinical Decision Support
          </div>

          <h1
            style={{
              fontSize: "clamp(2.5rem, 6vw, 5rem)",
              fontWeight: 800,
              lineHeight: 1.1,
              marginBottom: "1.5rem",
              color: "#f1f5f9",
            }}
          >
            AMR Intelligence
            <br />
            <span className="gradient-text">Powered by AI</span>
          </h1>

          <p
            style={{
              fontSize: "1.1rem",
              color: "#94a3b8",
              maxWidth: 520,
              lineHeight: 1.7,
              marginBottom: "3rem",
            }}
          >
            A 5-agent LangGraph pipeline that predicts antibiotic resistance,
            verifies genomic evidence via CARD database, and autonomously
            manages clinical supply chains.
          </p>

          <motion.button
            data-hover
            whileHover={{ scale: 1.05 }}
            whileTap={{ scale: 0.98 }}
            onClick={() => setStarted(true)}
            style={{
              background: "linear-gradient(135deg, #7c3aed, #06b6d4)",
              border: "none",
              color: "white",
              padding: "14px 40px",
              borderRadius: 12,
              fontSize: "1rem",
              fontWeight: 600,
              cursor: "none",
              marginBottom: "1rem",
            }}
          >
            Launch Clinical Dashboard →
          </motion.button>
        </motion.div>

        {/* Agent Pipeline Preview */}
        <motion.div
          initial={{ opacity: 0, y: 40 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, delay: 0.6 }}
          className="flex items-center gap-3 flex-wrap justify-center"
          style={{ marginTop: "5rem" }}
        >
          {agents.map((agent, i) => (
            <div key={agent.label} className="flex items-center gap-3">
              <motion.div
                data-hover
                whileHover={{ scale: 1.05, y: -2 }}
                className="glass"
                style={{
                  padding: "12px 20px",
                  display: "flex",
                  alignItems: "center",
                  gap: 10,
                }}
              >
                <div
                  style={{
                    width: 32,
                    height: 32,
                    background: `${agent.color}20`,
                    border: `1px solid ${agent.color}40`,
                    borderRadius: 8,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
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
              </motion.div>

              {i < agents.length - 1 && (
                <motion.div
                  animate={{ opacity: [0.3, 1, 0.3] }}
                  transition={{
                    duration: 1.5,
                    repeat: Infinity,
                    delay: i * 0.2,
                  }}
                  style={{ color: "#475569", fontSize: "1.2rem" }}
                >
                  →
                </motion.div>
              )}
            </div>
          ))}
        </motion.div>
      </div>
    </main>
  );
}
