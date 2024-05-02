setInterval(() => {
    chrome.runtime.sendMessage({ type: "ping" });
}, 5000);