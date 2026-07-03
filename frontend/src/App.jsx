import { useState, useEffect, useRef } from "react";
import axios from "axios";
import ChatMessage from "./components/ChatMessage";
import IngestBar from "./components/IngestBar";
import Sidebar from "./components/Sidebar";
import "./App.css";

function App() {
  const [messages, setMessages] = useState([
    {
      role: "assistant",
      content: "Welcome to your personal knowledge base. Add content using the bar above, then ask me anything about it."
    }
  ]);
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [chunkCount, setChunkCount] = useState(0);
  const [sources, setSources] = useState([]);
  const bottomRef = useRef(null);

  const refreshStatus = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:8000/status");
      setChunkCount(res.data.chunks_stored);
    } catch (err) {
      console.error("Could not reach API", err);
    }
  };

  const refreshSources = async () => {
    try {
      const res = await axios.get("http://127.0.0.1:8000/sources");
      setSources(res.data.sources);
    } catch (err) {
      console.error("Could not fetch sources", err);
    }
  };

  const handleDelete = (deletedName) => {
    setSources(prev => prev.filter(s => s.name !== deletedName));
  };

  useEffect(() => {
    refreshStatus();
    refreshSources();
  }, []);

  useEffect(() => {
    bottomRef.current?.scrollIntoView({ behavior: "smooth" });
  }, [messages]);

  const sendMessage = async () => {
    if (!input.trim() || loading) return;

    const question = input.trim();
    setInput("");
    setMessages(prev => [...prev, { role: "user", content: question }]);
    setLoading(true);

    try {
      const res = await axios.post("http://127.0.0.1:8000/chat", {
        question,
        top_k: 3
      });
      setMessages(prev => [...prev, {
        role: "assistant",
        content: res.data.answer,
        sources: res.data.sources
      }]);
    } catch (err) {
      const detail = err.response?.data?.detail || "Something went wrong.";
      setMessages(prev => [...prev, {
        role: "assistant",
        content: detail
      }]);
    } finally {
      setLoading(false);
    }
  };

  const onIngested = () => {
    refreshStatus();
    refreshSources();
  };

  return (
    <div style={{
      display: "flex",
      flexDirection: "column",
      height: "100vh",
      background: "#f5f2ee"
    }}>

      {/* Header */}
      <div style={{
        padding: "18px 28px",
        background: "#4a6741",
        display: "flex",
        justifyContent: "space-between",
        alignItems: "center",
        flexShrink: 0
      }}>
        <div>
          <div style={{
            fontSize: "20px",
            fontWeight: "700",
            color: "#fff",
            fontFamily: "Georgia, serif",
            letterSpacing: "0.3px"
          }}>
            Knowledge Base
          </div>
          <div style={{
            fontSize: "11px",
            color: "#c5d4bf",
            fontFamily: "system-ui, sans-serif",
            letterSpacing: "1px",
            textTransform: "uppercase",
            marginTop: "2px"
          }}>
            Your AI-powered second brain
          </div>
        </div>

        <div style={{
          fontSize: "12px",
          color: chunkCount > 0 ? "#fff" : "#c5d4bf",
          background: "rgba(255,255,255,0.15)",
          padding: "6px 14px",
          borderRadius: "20px",
          fontFamily: "system-ui, sans-serif",
          border: "1px solid rgba(255,255,255,0.2)"
        }}>
          {chunkCount > 0 ? `${chunkCount} chunks stored` : "Empty"}
        </div>
      </div>

      {/* Ingest Bar */}
      <IngestBar onIngested={onIngested} />

      {/* Main Body — Sidebar + Chat */}
      <div style={{
        display: "flex",
        flex: 1,
        overflow: "hidden"
      }}>

        {/* Sidebar */}
        <Sidebar
          sources={sources}
          onDelete={handleDelete}
          onRefresh={refreshSources}
        />

        {/* Chat Column */}
        <div style={{
          display: "flex",
          flexDirection: "column",
          flex: 1,
          overflow: "hidden"
        }}>

          {/* Chat Area */}
          <div style={{
            flex: 1,
            overflowY: "auto",
            padding: "28px 32px",
            background: "#f5f2ee",
            display: "flex",
            flexDirection: "column",
            alignItems: "center"
          }}>
            <div style={{ width: "100%", maxWidth: "720px" }}>

              {messages.map((msg, i) => (
                <ChatMessage key={i} message={msg} />
              ))}

              {loading && (
                <div style={{
                  display: "flex",
                  alignItems: "center",
                  gap: "10px",
                  color: "#8a9e82",
                  fontSize: "13px",
                  fontFamily: "system-ui, sans-serif",
                  padding: "8px 0"
                }}>
                  <div style={{
                    width: "8px",
                    height: "8px",
                    borderRadius: "50%",
                    background: "#7a9e6e"
                  }} />
                  Searching and thinking...
                </div>
              )}

              <div ref={bottomRef} />
            </div>
          </div>

          {/* Input Bar */}
          <div style={{
            padding: "18px 28px",
            background: "#eee8e0",
            borderTop: "1px solid #d9d2c8",
            display: "flex",
            justifyContent: "center",
            flexShrink: 0
          }}>
            <div style={{
              width: "100%",
              maxWidth: "720px",
              display: "flex",
              gap: "12px",
              alignItems: "center"
            }}>
              <input
                value={input}
                onChange={e => setInput(e.target.value)}
                onKeyDown={e => e.key === "Enter" && sendMessage()}
                placeholder="Ask anything about your knowledge base..."
                disabled={loading}
                style={{
                  flex: 1,
                  padding: "13px 18px",
                  borderRadius: "12px",
                  border: "1px solid #d9d2c8",
                  background: "#faf8f5",
                  color: "#2c2c2c",
                  fontSize: "14px",
                  fontFamily: "system-ui, sans-serif",
                  boxShadow: "0 1px 3px rgba(0,0,0,0.05)"
                }}
              />
              <button
                onClick={sendMessage}
                disabled={loading}
                style={{
                  padding: "13px 28px",
                  borderRadius: "12px",
                  border: "none",
                  background: loading ? "#a8b89a" : "#4a6741",
                  color: "#fff",
                  cursor: loading ? "not-allowed" : "pointer",
                  fontSize: "14px",
                  fontFamily: "Georgia, serif",
                  letterSpacing: "0.3px",
                  boxShadow: "0 2px 6px rgba(74,103,65,0.3)"
                }}
              >
                {loading ? "Thinking..." : "Send"}
              </button>
            </div>
          </div>

        </div>
        {/* End Chat Column */}

      </div>
      {/* End Main Body */}

    </div>
  );
}

export default App;