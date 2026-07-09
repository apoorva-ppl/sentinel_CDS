"use client";

import { useState, useRef, useEffect } from "react";
import { motion, AnimatePresence } from "framer-motion";
import { Send, Bot, User, Loader2 } from "lucide-react";

interface Message {
  role: "user" | "assistant";
  content: string;
}

interface Props {
  result: any;
}

export default function Copilot({ result }: Props) {
  const [messages, setMessages] = useState<Message[]>([
    {
      role: "assistant",
      content: `Analysis complete. I've reviewed the resistance profile for **${result.isolate_id}**. Selected therapy: **${result.selected_therapy}**. How can I help you interpret these results?`,
    },
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const bottomRef = useRef<HTMLDivElement>(null);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const userMsg = input.trim();
    setInput("");
    setMessages((prev) => [...prev, { role: "user", content: userMsg }]);
    setLoading(true);

    try {
      const res = await fetch("http://localhost:8000/api/chat", {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          message: userMsg,
          context: result,
          history: messages.map((m) => ({ role: m.role, content: m.content })),
        }),
      });
      const data = await res.json();
      setMessages((prev) => [
        ...prev,
        { role: "assistant", content: data.reply },
      ]);
    } catch (e) {
      setMessages((prev) => [
        ...prev,
        {
          role: "assistant",
          content: "Connection error. Please ensure the backend is running.",
        },
      ]);
    } finally {
      setLoading(false);
    }
  };

  return (
    <motion.div
      className="glass"
      style={{ height: 600, display: "flex", flexDirection: "column" }}
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
    >
      {/* Header */}
      <div
        style={{
          padding: "16px 20px",
          borderBottom: "1px solid rgba(124,58,237,0.15)",
          display: "flex",
          alignItems: "center",
          gap: 10,
        }}
      >
        <div
          style={{
            width: 34,
            height: 34,
            background: "linear-gradient(135deg, #ec4899, #7c3aed)",
            borderRadius: 10,
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
          }}
        >
          <Bot size={16} color="white" />
        </div>
        <div>
          <div
            style={{ fontSize: "0.85rem", fontWeight: 700, color: "#f1f5f9" }}
          >
            Sentinel Copilot
          </div>
          <div style={{ fontSize: "0.7rem", color: "#10b981" }}>
            ● Grounded in WHO AMR Guidelines
          </div>
        </div>
      </div>

      {/* Messages */}
      <div
        style={{
          flex: 1,
          overflowY: "auto",
          padding: "16px 20px",
          display: "flex",
          flexDirection: "column",
          gap: 12,
        }}
      >
        <AnimatePresence>
          {messages.map((msg, i) => (
            <motion.div
              key={i}
              initial={{ opacity: 0, y: 10 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ duration: 0.3 }}
              style={{
                display: "flex",
                gap: 10,
                justifyContent: msg.role === "user" ? "flex-end" : "flex-start",
              }}
            >
              {msg.role === "assistant" && (
                <div
                  style={{
                    width: 28,
                    height: 28,
                    flexShrink: 0,
                    background: "linear-gradient(135deg, #ec4899, #7c3aed)",
                    borderRadius: 8,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                  }}
                >
                  <Bot size={14} color="white" />
                </div>
              )}

              <div
                style={{
                  maxWidth: "75%",
                  padding: "10px 14px",
                  borderRadius:
                    msg.role === "user"
                      ? "12px 12px 4px 12px"
                      : "12px 12px 12px 4px",
                  background:
                    msg.role === "user"
                      ? "linear-gradient(135deg, #7c3aed, #06b6d4)"
                      : "rgba(255,255,255,0.04)",
                  border:
                    msg.role === "assistant"
                      ? "1px solid rgba(124,58,237,0.15)"
                      : "none",
                  fontSize: "0.82rem",
                  color: "#f1f5f9",
                  lineHeight: 1.6,
                }}
              >
                {msg.content}
              </div>

              {msg.role === "user" && (
                <div
                  style={{
                    width: 28,
                    height: 28,
                    flexShrink: 0,
                    background: "rgba(124,58,237,0.2)",
                    borderRadius: 8,
                    display: "flex",
                    alignItems: "center",
                    justifyContent: "center",
                  }}
                >
                  <User size={14} color="#7c3aed" />
                </div>
              )}
            </motion.div>
          ))}
        </AnimatePresence>

        {loading && (
          <motion.div
            initial={{ opacity: 0 }}
            animate={{ opacity: 1 }}
            style={{ display: "flex", gap: 10, alignItems: "center" }}
          >
            <div
              style={{
                width: 28,
                height: 28,
                background: "linear-gradient(135deg, #ec4899, #7c3aed)",
                borderRadius: 8,
                display: "flex",
                alignItems: "center",
                justifyContent: "center",
              }}
            >
              <Bot size={14} color="white" />
            </div>
            <div
              style={{
                padding: "10px 14px",
                background: "rgba(255,255,255,0.04)",
                border: "1px solid rgba(124,58,237,0.15)",
                borderRadius: "12px 12px 12px 4px",
                display: "flex",
                gap: 4,
                alignItems: "center",
              }}
            >
              {[0, 1, 2].map((i) => (
                <motion.div
                  key={i}
                  animate={{ y: [0, -4, 0] }}
                  transition={{
                    duration: 0.6,
                    repeat: Infinity,
                    delay: i * 0.15,
                  }}
                  style={{
                    width: 6,
                    height: 6,
                    borderRadius: "50%",
                    background: "#7c3aed",
                  }}
                />
              ))}
            </div>
          </motion.div>
        )}
        <div ref={bottomRef} />
      </div>

      {/* Input */}
      <div
        style={{
          padding: "12px 16px",
          borderTop: "1px solid rgba(124,58,237,0.15)",
          display: "flex",
          gap: 10,
        }}
      >
        <input
          value={input}
          onChange={(e) => setInput(e.target.value)}
          onKeyDown={(e) => e.key === "Enter" && sendMessage()}
          placeholder="Ask about resistance mechanisms, dosing, alternatives..."
          style={{
            flex: 1,
            background: "rgba(255,255,255,0.03)",
            border: "1px solid rgba(124,58,237,0.2)",
            borderRadius: 10,
            padding: "10px 14px",
            color: "#f1f5f9",
            fontSize: "0.85rem",
            outline: "none",
            cursor: "none",
          }}
        />
        <motion.button
          data-hover
          whileHover={{ scale: 1.05 }}
          whileTap={{ scale: 0.95 }}
          onClick={sendMessage}
          disabled={loading || !input.trim()}
          style={{
            width: 42,
            height: 42,
            borderRadius: 10,
            border: "none",
            background: "linear-gradient(135deg, #7c3aed, #06b6d4)",
            cursor: "none",
            display: "flex",
            alignItems: "center",
            justifyContent: "center",
            opacity: loading || !input.trim() ? 0.5 : 1,
          }}
        >
          <Send size={16} color="white" />
        </motion.button>
      </div>
    </motion.div>
  );
}
