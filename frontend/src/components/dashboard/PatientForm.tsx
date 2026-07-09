"use client";

import { useState } from "react";
import { motion } from "framer-motion";
import { Loader2, FlaskConical } from "lucide-react";

interface Props {
  onSubmit: (data: any) => void;
  loading: boolean;
}

const inputStyle = {
  width: "100%",
  background: "rgba(255,255,255,0.03)",
  border: "1px solid rgba(124,58,237,0.2)",
  borderRadius: 8,
  padding: "10px 14px",
  color: "#f1f5f9",
  fontSize: "0.875rem",
  outline: "none",
  cursor: "none",
};

const labelStyle = {
  fontSize: "0.75rem",
  color: "#94a3b8",
  marginBottom: 6,
  display: "block",
  fontWeight: 500,
};

export default function PatientForm({ onSubmit, loading }: Props) {
  const [form, setForm] = useState({
    isolate_id: "Escherichia coli",
    Age: 45,
    Gender: 1,
    Diabetes: 0,
    Infection_Freq: 2,
    Hospital_before: false,
    Hypertension: false,
    Penicillin_Allergy: false,
    Renal_Impaired: false,
  });

  const handleSubmit = () => {
    onSubmit({
      isolate_id: form.isolate_id,
      patient_profile: {
        Age: form.Age,
        Gender: form.Gender,
        Diabetes: form.Diabetes,
        Infection_Freq: form.Infection_Freq,
        Hospital_before: form.Hospital_before,
        Hypertension: form.Hypertension,
        Penicillin_Allergy: form.Penicillin_Allergy,
        Renal_Impaired: form.Renal_Impaired,
      },
    });
  };

  return (
    <motion.div
      initial={{ opacity: 0, x: -20 }}
      animate={{ opacity: 1, x: 0 }}
      transition={{ duration: 0.5 }}
      className="glass"
      style={{ padding: 24 }}
    >
      <div className="flex items-center gap-2" style={{ marginBottom: 24 }}>
        <FlaskConical size={18} color="#7c3aed" />
        <span
          style={{ fontWeight: 700, fontSize: "0.95rem", color: "#f1f5f9" }}
        >
          Patient Profile
        </span>
      </div>

      <div style={{ display: "flex", flexDirection: "column", gap: 16 }}>
        {/* Isolate ID */}
        <div>
          <label style={labelStyle}>Bacterial Isolate / Strain</label>
          <input
            style={inputStyle}
            value={form.isolate_id}
            onChange={(e) => setForm({ ...form, isolate_id: e.target.value })}
            placeholder="e.g. Escherichia coli"
          />
        </div>

        {/* Age */}
        <div>
          <label style={labelStyle}>Age — {form.Age} years</label>
          <input
            type="range"
            min={0}
            max={100}
            value={form.Age}
            onChange={(e) => setForm({ ...form, Age: +e.target.value })}
            style={{ width: "100%", accentColor: "#7c3aed", cursor: "none" }}
          />
        </div>

        {/* Infection Freq */}
        <div>
          <label style={labelStyle}>
            Infection Frequency — {form.Infection_Freq}x/year
          </label>
          <input
            type="range"
            min={0}
            max={10}
            value={form.Infection_Freq}
            onChange={(e) =>
              setForm({ ...form, Infection_Freq: +e.target.value })
            }
            style={{ width: "100%", accentColor: "#7c3aed", cursor: "none" }}
          />
        </div>

        {/* Gender */}
        <div>
          <label style={labelStyle}>Gender</label>
          <select
            style={{ ...inputStyle, cursor: "none" }}
            value={form.Gender}
            onChange={(e) => setForm({ ...form, Gender: +e.target.value })}
          >
            <option value={1}>Male</option>
            <option value={0}>Female</option>
          </select>
        </div>

        {/* Toggles */}
        {[
          { key: "Hospital_before", label: "Prior Hospitalization" },
          { key: "Diabetes", label: "Diabetes" },
          { key: "Hypertension", label: "Hypertension" },
          { key: "Penicillin_Allergy", label: "Penicillin Allergy" },
          { key: "Renal_Impaired", label: "Renal Impairment" },
        ].map(({ key, label }) => (
          <div key={key} className="flex items-center justify-between">
            <label style={{ ...labelStyle, marginBottom: 0 }}>{label}</label>
            <motion.div
              data-hover
              whileTap={{ scale: 0.95 }}
              onClick={() => setForm({ ...form, [key]: !(form as any)[key] })}
              style={{
                width: 44,
                height: 24,
                borderRadius: 12,
                background: (form as any)[key]
                  ? "linear-gradient(135deg, #7c3aed, #06b6d4)"
                  : "rgba(255,255,255,0.05)",
                border: "1px solid rgba(124,58,237,0.3)",
                cursor: "none",
                position: "relative",
                transition: "all 0.2s",
              }}
            >
              <motion.div
                animate={{ x: (form as any)[key] ? 20 : 2 }}
                transition={{ type: "spring", stiffness: 500, damping: 30 }}
                style={{
                  width: 18,
                  height: 18,
                  background: "white",
                  borderRadius: "50%",
                  position: "absolute",
                  top: 2,
                }}
              />
            </motion.div>
          </div>
        ))}

        {/* Submit */}
        <motion.button
          data-hover
          whileHover={{ scale: 1.02 }}
          whileTap={{ scale: 0.98 }}
          onClick={handleSubmit}
          disabled={loading}
          style={{
            width: "100%",
            padding: "12px",
            borderRadius: 10,
            border: "none",
            background: loading
              ? "rgba(124,58,237,0.3)"
              : "linear-gradient(135deg, #7c3aed, #06b6d4)",
            color: "white",
            fontWeight: 600,
            fontSize: "0.9rem",
            cursor: "none",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            gap: 8,
            marginTop: 8,
          }}
        >
          {loading ? (
            <>
              <motion.div
                animate={{ rotate: 360 }}
                transition={{ duration: 1, repeat: Infinity, ease: "linear" }}
              >
                <Loader2 size={16} />
              </motion.div>
              Analyzing...
            </>
          ) : (
            "Run Analysis →"
          )}
        </motion.button>
      </div>
    </motion.div>
  );
}
