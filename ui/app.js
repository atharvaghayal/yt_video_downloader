async function downloadVideo() {
  const url = document.getElementById('urlInput').value.trim();
  const status = document.getElementById('status');
  if (!url) {
    status.innerText = "Please enter a valid URL.";
    return;
  }

  status.innerText = "⏳ Downloading...";

  // Call the FastAPI backend to process video download
  const response = await fetch("http://127.0.0.1:8000/download/", {
    method: "POST",
    headers: {
      "Content-Type": "application/json",
    },
    body: JSON.stringify({ "url": url })
  });

  if (response.ok) {
    const result = await response.json();
    // Trigger file download
    status.innerText = "✅ Download Complete!";
    const downloadUrl = result.download_url;

    // Create a temporary link to start downloading
    const a = document.createElement("a");
    a.href = downloadUrl;
    a.download = downloadUrl.split('/').pop();
    a.click();
  } else {
    const error = await response.json();
    status.innerText = `❌ Error: ${error.detail}`;
  }
}