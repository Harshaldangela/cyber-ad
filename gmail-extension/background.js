// Store and retrieve settings
chrome.runtime.onInstalled.addListener(() => {
  chrome.storage.sync.get({ cyberad_backend: 'http://localhost:8007' }, (cfg) => {
    if (!cfg.cyberad_backend) {
      chrome.storage.sync.set({ cyberad_backend: 'http://localhost:8007' });
    }
  });
});

// Message router
chrome.runtime.onMessage.addListener((msg, sender, sendResponse) => {
  if (msg && msg.type === 'GENERATE_AD') {
    chrome.storage.sync.get(['cyberad_backend'], async (res) => {
      const base = res.cyberad_backend || 'http://localhost:8007';
      try {
        const r = await fetch(`${base}/analyze`, {
          method: 'POST',
          headers: { 'Content-Type': 'application/json' },
          body: JSON.stringify({ text: msg.text })
        });
        const data = await r.json();
        if (!r.ok) throw new Error(data.detail || 'Request failed');
        sendResponse({ ok: true, result: data });
      } catch (e) {
        sendResponse({ ok: false, error: e.message });
      }
    });
    return true; // async response
  }
});