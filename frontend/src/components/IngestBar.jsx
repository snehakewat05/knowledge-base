import { useState } from "react";
import axios from "axios";

function IngestBar({ onIngested }) {
  const [input, setInput] = useState("");
  const [loading, setLoading] = useState(false);
  const [message, setMessage] = useState("");

  const handleIngest = async () => {
    if (!input.trim()) return;
    setLoading(true);
    setMessage("");

    try {
      await axios.post("http://127.0.0.1:8000/ingest/url", { url: input });
      setMessage("Ingested successfully");
      setInput("");
      onIngested();
    } catch (err) {
      setMessage(`Failed: ${err.response?.data?.detail || err.message}`);
    } finally {
      setLoading(false);
    }
  };

  const handleFileUpload = async (e) => {
    const file = e.target.files[0];
    if (!file) return;
    setLoading(true);
    setMessage("");

    const formData = new FormData();
    formData.append("file", file);

    try {
      await axios.post("http://127.0.0.1:8000/ingest/file", formData);
      setMessage(`${file.name} ingested successfully`);
      onIngested();
    } catch (err) {
      setMessage(`Failed: ${err.response?.data?.detail || err.message}`);
    } finally {
      setLoading(false);
    }
  };

  return (
    <div style={{
      padding: "14px 24px",
      background: "#eee8e0",
      borderBottom: "1px solid #d9d2c8"
    }}>
      <div style={{
        fontSize: "10px",
        letterSpacing: "1.5px",
        color: "#8a9e82",
        marginBottom: "8px",
        textTransform: "uppercase",
        fontFamily: "system-ui, sans-serif"
      }}>
        Add to knowledge base
      </div>

      <div style={{ display: "flex", gap: "8px" }}>
        <input
          value={input}
          onChange={e => setInput(e.target.value)}
          onKeyDown={e => e.key === "Enter" && handleIngest()}
          placeholder="Paste a URL or YouTube link..."
          disabled={loading}
          style={{
            flex: 1,
            padding: "10px 14px",
            borderRadius: "8px",
            border: "1px solid #d9d2c8",
            background: "#faf8f5",
            color: "#2c2c2c",
            fontSize: "13px",
            fontFamily: "system-ui, sans-serif"
          }}
        />
        <button
          onClick={handleIngest}
          disabled={loading}
          style={{
            padding: "10px 20px",
            borderRadius: "8px",
            border: "none",
            background: loading ? "#a8b89a" : "#4a6741",
            color: "#fff",
            cursor: loading ? "not-allowed" : "pointer",
            fontSize: "13px",
            fontFamily: "system-ui, sans-serif",
            letterSpacing: "0.3px"
          }}
        >
          {loading ? "Adding..." : "Add"}
        </button>

        <label style={{
          padding: "10px 20px",
          borderRadius: "8px",
          border: "1px solid #d9d2c8",
          background: "#faf8f5",
          color: "#4a6741",
          cursor: "pointer",
          fontSize: "13px",
          fontFamily: "system-ui, sans-serif",
          whiteSpace: "nowrap"
        }}>
          Upload File
          <input
            type="file"
            accept=".txt,.pdf,.md"
            onChange={handleFileUpload}
            style={{ display: "none" }}
          />
        </label>
      </div>

      {message && (
        <div style={{
          marginTop: "8px",
          fontSize: "12px",
          color: message.includes("Failed") ? "#b85c5c" : "#4a6741",
          fontFamily: "system-ui, sans-serif"
        }}>
          {message}
        </div>
      )}
    </div>
  );
}

export default IngestBar;