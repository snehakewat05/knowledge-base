function ChatMessage({ message }) {
  const isUser = message.role === "user";

  return (
    <div style={{
      display: "flex",
      justifyContent: isUser ? "flex-end" : "flex-start",
      marginBottom: "20px",
      gap: "10px",
      alignItems: "flex-start"
    }}>

      {/* Avatar — only for assistant */}
      {!isUser && (
        <div style={{
          width: "32px",
          height: "32px",
          borderRadius: "50%",
          background: "#4a6741",
          flexShrink: 0,
          display: "flex",
          alignItems: "center",
          justifyContent: "center",
          fontSize: "13px",
          color: "#fff",
          fontFamily: "Georgia, serif",
          marginTop: "4px"
        }}>
          K
        </div>
      )}

      <div style={{ maxWidth: "72%" }}>
        {/* Message bubble */}
        <div style={{
          padding: "14px 18px",
          borderRadius: isUser
            ? "20px 20px 4px 20px"
            : "20px 20px 20px 4px",
          background: isUser ? "#4a6741" : "#ffffff",
          color: isUser ? "#fff" : "#2c2c2c",
          fontSize: "14px",
          lineHeight: "1.7",
          boxShadow: "0 1px 4px rgba(0,0,0,0.08)",
          border: isUser ? "none" : "1px solid #e0dbd3"
        }}>
          {message.content}
        </div>

        {/* Source cards */}
        {message.sources && message.sources.length > 0 && (
          <div style={{ marginTop: "10px" }}>
            <div style={{
              fontSize: "10px",
              letterSpacing: "1.5px",
              color: "#8a9e82",
              marginBottom: "8px",
              fontFamily: "system-ui, sans-serif",
              textTransform: "uppercase"
            }}>
              Sources
            </div>
            {message.sources.map((source, i) => (
              <div key={i} style={{
                background: "#fff",
                border: "1px solid #e0dbd3",
                borderLeft: "3px solid #7a9e6e",
                borderRadius: "8px",
                padding: "10px 14px",
                marginBottom: "8px",
                fontSize: "12px",
                boxShadow: "0 1px 3px rgba(0,0,0,0.05)"
              }}>
                <div style={{
                  color: "#4a6741",
                  fontWeight: "600",
                  marginBottom: "4px",
                  fontFamily: "system-ui, sans-serif",
                  display: "flex",
                  justifyContent: "space-between"
                }}>
                  <span>
                    {source.source}
                    {source.page_number && ` — p.${source.page_number}`}
                  </span>
                  <span style={{
                    color: "#a8b89a",
                    fontWeight: "400"
                  }}>
                    {Math.round(source.relevance_score * 100)}% match
                  </span>
                </div>
                <div style={{ color: "#6b6b6b", lineHeight: "1.5" }}>
                  {source.text.slice(0, 130)}...
                </div>
              </div>
            ))}
          </div>
        )}
      </div>
    </div>
  );
}

export default ChatMessage;