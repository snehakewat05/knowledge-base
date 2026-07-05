import { useState } from "react";
import axios from "axios";

function Sidebar({ sources, onDelete, onRefresh }) {
  const [deleting, setDeleting] = useState(null);

  const handleDelete = async (sourceName) => {
    setDeleting(sourceName);
    try {
      await axios.delete(
        `http://127.0.0.1:8000/sources/${encodeURIComponent(sourceName)}`
      );
      onDelete(sourceName);
      onRefresh();
    } catch (err) {
      console.error("Delete failed:", err);
    } finally {
      setDeleting(null);
    }
  };

  const getSourceIcon = (name) => {
    if (name.includes("youtube")) return "YT";
    if (name.endsWith(".pdf")) return "PDF";
    if (name.endsWith(".txt")) return "TXT";
    if (name.endsWith(".md")) return "MD";
    return "URL";
  };

  const getIconColor = (name) => {
    if (name.includes("youtube")) return "#b85c5c";
    if (name.endsWith(".pdf")) return "#c47a3a";
    if (name.endsWith(".txt")) return "#4a6741";
    if (name.endsWith(".md")) return "#5a6e8a";
    return "#7a6e9e";
  };

  const truncateName = (name, max = 24) => {
    if (name.length <= max) return name;
    return name.slice(0, max) + "...";
  };

  return (
    <div style={{
      width: "240px",
      minWidth: "240px",
      background: "#f0ece4",
      borderRight: "1px solid #d9d2c8",
      display: "flex",
      flexDirection: "column",
      height: "100%"
    }}>

      {/* Sidebar Header */}
      <div style={{
        padding: "18px 16px 12px",
        borderBottom: "1px solid #d9d2c8"
      }}>
        <div style={{
          fontSize: "10px",
          letterSpacing: "1.5px",
          color: "#8a9e82",
          textTransform: "uppercase",
          fontFamily: "system-ui, sans-serif"
        }}>
          Knowledge Library
        </div>
      </div>

      {/* Source List */}
      <div style={{
        flex: 1,
        overflowY: "auto",
        padding: "10px 8px"
      }}>
        {sources.length === 0 ? (
          <div style={{
            padding: "20px 12px",
            fontSize: "12px",
            color: "#a89e8e",
            fontFamily: "system-ui, sans-serif",
            lineHeight: "1.6",
            textAlign: "center"
          }}>
            Nothing ingested yet. Add a file or URL above.
          </div>
        ) : (
          sources.map((source, i) => (
            <div key={i} style={{
              display: "flex",
              alignItems: "center",
              gap: "8px",
              padding: "8px 10px",
              borderRadius: "8px",
              marginBottom: "4px",
              background: "transparent",
              transition: "background 0.15s",
              cursor: "default",
            }}
              onMouseEnter={e => e.currentTarget.style.background = "#e8e2d8"}
              onMouseLeave={e => e.currentTarget.style.background = "transparent"}
            >
              {/* Type badge */}
              <div style={{
                fontSize: "9px",
                fontWeight: "700",
                color: "#fff",
                background: getIconColor(source.name),
                padding: "2px 5px",
                borderRadius: "4px",
                fontFamily: "system-ui, sans-serif",
                flexShrink: 0,
                letterSpacing: "0.3px"
              }}>
                {getSourceIcon(source.name)}
              </div>

              {/* Source name + chunk count + tags */}
              <div style={{ flex: 1, minWidth: 0 }}>
                <div style={{
                  fontSize: "12px",
                  color: "#2c2c2c",
                  fontFamily: "system-ui, sans-serif",
                  whiteSpace: "nowrap",
                  overflow: "hidden",
                  textOverflow: "ellipsis"
                }}>
                  {truncateName(source.name)}
                </div>
                <div style={{
                  fontSize: "10px",
                  color: "#a89e8e",
                  fontFamily: "system-ui, sans-serif",
                  marginTop: "1px"
                }}>
                  {source.chunk_count} chunks
                </div>

                {/* Tags */}
                {source.tags && source.tags.length > 0 && (
                  <div style={{
                    display: "flex",
                    flexWrap: "wrap",
                    gap: "3px",
                    marginTop: "4px"
                  }}>
                    {source.tags.slice(0, 3).map((tag, t) => (
                      <span key={t} style={{
                        fontSize: "9px",
                        background: "#e0dbd3",
                        color: "#4a6741",
                        padding: "1px 5px",
                        borderRadius: "4px",
                        fontFamily: "system-ui, sans-serif"
                      }}>
                        {tag}
                      </span>
                    ))}
                  </div>
                )}
              </div>

              {/* Remove button */}
              <button
                onClick={() => handleDelete(source.name)}
                disabled={deleting === source.name}
                title="Remove from knowledge base"
                style={{
                  width: "20px",
                  height: "20px",
                  borderRadius: "50%",
                  border: "1px solid #d9d2c8",
                  background: deleting === source.name ? "#e8e2d8" : "#faf8f5",
                  color: "#b85c5c",
                  cursor: deleting === source.name ? "not-allowed" : "pointer",
                  fontSize: "14px",
                  lineHeight: "1",
                  display: "flex",
                  alignItems: "center",
                  justifyContent: "center",
                  flexShrink: 0,
                  fontFamily: "system-ui, sans-serif"
                }}
              >
                {deleting === source.name ? "..." : "-"}
              </button>
            </div>
          ))
        )}
      </div>

      {/* Footer */}
      <div style={{
        padding: "12px 16px",
        borderTop: "1px solid #d9d2c8",
        fontSize: "11px",
        color: "#a89e8e",
        fontFamily: "system-ui, sans-serif"
      }}>
        {sources.length} source{sources.length !== 1 ? "s" : ""} stored
      </div>

    </div>
  );
}

export default Sidebar;