"use client";

import { useState } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Activity, ArrowLeft, Loader2 } from "lucide-react";
import PatientForm from "./PatientForm";
import AgentPipeline from "./AgentPipeline";
import DrugChart from "./DrugChart";
import Copilot from "../chat/Copilot";

export default function Dashboard() {
  const [result, setResult] = useState<any>(null);
  const [loading, setLoading] = useState(false);
  const [activeTab, setActiveTab] = useState<"results" | "chat">("results");

  const handleAnalysis = async (formData: any) => {
    setLoading(true);
    try {
      const res = await fetch("http://localhost:8000/api/analyze", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(formData),
      });
      const data = await res.json();
      setResult(data);
    } catch (e) {
      console.error(e);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{ minHeight: "100vh", background: "#0a0a0f" }}>
      {/* Header */}
      <div
        className="flex items-center justify-between px-8 py-5"
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

        {/* Tabs */}
        {result && (
          <div
            className="flex gap-2"
            style={{
              background: "rgba(18,18,31,0.8)",
              padding: "4px",
              borderRadius: 10,
              border: "1px solid rgba(124,58,237,0.2)",
            }}
          >
            {["results", "chat"].map((tab) => (
              <button
                key={tab}
                data-hover
                onClick={() => setActiveTab(tab as any)}
                style={{
                  padding: "6px 16px",
                  borderRadius: 7,
                  border: "none",
                  cursor: "none",
                  fontSize: "0.8rem",
                  fontWeight: 600,
                  background:
                    activeTab === tab
                      ? "linear-gradient(135deg, #7c3aed, #06b6d4)"
                      : "transparent",
                  color: activeTab === tab ? "white" : "#64748b",
                  transition: "all 0.2s",
                }}
              >
                {tab === "results" ? "Analysis" : "AI Copilot"}
              </button>
            ))}
          </div>
        )}

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
      </div>

      {/* Main Content */}
      <div
        className="flex gap-6 p-8"
        style={{ maxWidth: 1400, margin: "0 auto" }}
      >
        {/* Left — Patient Form */}
        <div style={{ width: 360, flexShrink: 0 }}>
          <PatientForm onSubmit={handleAnalysis} loading={loading} />
        </div>

        {/* Right — Results */}
        <div style={{ flex: 1 }}>
          <AnimatePresence mode="wait">
            {loading && (
              <motion.div
                key="loading"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                exit={{ opacity: 0 }}
                className="flex flex-col items-center justify-center"
                style={{ height: 400, gap: 16 }}
              >
                <motion.div
                  animate={{ rotate: 360 }}
                  transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
                >
                  <Loader2 size={40} color="#7c3aed" />
                </motion.div>
                <p style={{ color: "#94a3b8", fontSize: "0.9rem" }}>
                  Running 5-agent pipeline...
                </p>
              </motion.div>
            )}

            {!loading && !result && (
              <motion.div
                key="empty"
                initial={{ opacity: 0 }}
                animate={{ opacity: 1 }}
                className="flex flex-col items-center justify-center"
                style={{ height: 400, gap: 12 }}
              >
                <div
                  style={{
                    width: 64,
                    height: 64,
                    background: "rgba(124,58,237,0.1)",
                    border: "1px solid rgba(124,58,237,0.2)",
                    borderRadius: 16,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                  }}
                >
                  <Activity size={28} color="#7c3aed" />
                </div>
                <p style={{ color: "#94a3b8", fontSize: "0.9rem" }}>
                  Enter patient data to begin analysis
                </p>
              </motion.div>
            )}

            {!loading && result && (
              <motion.div
                key="results"
                initial={{ opacity: 0, y: 20 }}
                animate={{ opacity: 1, y: 0 }}
                transition={{ duration: 0.5 }}
              >
                {activeTab === "results" ? (
                  <div className="flex flex-col gap-6">
                    <AgentPipeline result={result} />
                    <DrugChart drugs={result.ml_15_drug_profile} />
                  </div>
                ) : (
                  <Copilot result={result} />
                )}
              </motion.div>
            )}
          </AnimatePresence>
        </div>
      </div>
    </div>
  );
}
