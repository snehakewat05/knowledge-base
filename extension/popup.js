const API_URL = "http://127.0.0.1:8000";

const clipBtn = document.getElementById("clipBtn");
const status = document.getElementById("status");
const urlPreview = document.getElementById("urlPreview");
const openAppBtn = document.getElementById("openAppBtn");

// Get the current tab's URL and show it
chrome.tabs.query({ active: true, currentWindow: true }, (tabs) => {
  const currentUrl = tabs[0].url;
  urlPreview.textContent = currentUrl;

  // Disable button for non-http pages
  if (!currentUrl.startsWith("http")) {
    clipBtn.disabled = true;
    status.textContent = "Cannot clip this type of page.";
    status.className = "status error";
  }
});

// Clip button — send URL to backend
clipBtn.addEventListener("click", async () => {
  chrome.tabs.query({ active: true, currentWindow: true }, async (tabs) => {
    const currentUrl = tabs[0].url;

    clipBtn.disabled = true;
    clipBtn.textContent = "Adding...";
    status.textContent = "";
    status.className = "status";

    try {
      const response = await fetch(`${API_URL}/ingest/url`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ url: currentUrl })
      });

      if (!response.ok) {
        const err = await response.json();
        throw new Error(err.detail || "Server error");
      }

      const data = await response.json();
      status.textContent = `Saved! ${data.chunks_stored} chunks stored.`;
      status.className = "status";
      clipBtn.textContent = "Added!";

    } catch (err) {
      status.textContent = `Failed: ${err.message}`;
      status.className = "status error";
      clipBtn.disabled = false;
      clipBtn.textContent = "Add to Knowledge Base";
    }
  });
});

// Open app button
openAppBtn.addEventListener("click", () => {
  chrome.tabs.create({ url: "http://localhost:5173" });
});