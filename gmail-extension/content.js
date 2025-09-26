// Backend calls are proxied via background to avoid page CSP/CORS issues

function findMessageBody() {
  const selectors = [
    'div.a3s.aiL',     // Gmail message body container
    'div.a3s',
  ];
  for (const sel of selectors) {
    const el = document.querySelector(sel);
    if (el) return el;
  }
  return null;
}

function extractVisibleText(el) {
  if (!el) return '';
  const clone = el.cloneNode(true);
  // remove quoted content
  clone.querySelectorAll('blockquote').forEach(b => b.remove());
  return clone.innerText.trim();
}

function createButton() {
  const btn = document.createElement('button');
  btn.textContent = 'Analyze & Generate';
  btn.style.cssText = 'margin:8px 0;padding:8px 12px;background:#0b5fff;color:#fff;border:none;border-radius:6px;cursor:pointer;';
  btn.addEventListener('click', async () => {
    const body = findMessageBody();
    const text = extractVisibleText(body);
    if (!text) {
      alert('Could not extract email text.');
      return;
    }
    btn.disabled = true;
    btn.textContent = 'Generating...';
    try {
      // Ask background to call /analyze (server will classify first)
      chrome.runtime.sendMessage({ type: 'GENERATE_AD', text }, (resp) => {
        if (!resp || !resp.ok) {
          alert('Error: ' + (resp && resp.error ? resp.error : 'Unknown error'));
          btn.disabled = false;
          btn.textContent = 'Analyze & Generate';
          return;
        }
        const result = resp.result || {};
        showResultFromAnalyze(result);
        btn.disabled = false;
        btn.textContent = 'Analyze & Generate';
      });
    } catch (e) {
      alert('Error: ' + e.message);
      btn.disabled = false;
      btn.textContent = 'Analyze & Generate';
    } finally {
      btn.disabled = false;
      btn.textContent = 'Analyze & Generate';
    }
  });
  return btn;
}

function showResultFromAnalyze(result) {
  const panel = document.createElement('div');
  panel.style.cssText = 'white-space:pre-wrap;background:#f3f4f6;border:1px solid #e5e7eb;padding:12px;border-radius:8px;margin-top:8px;';

  const status = document.createElement('div');
  status.style.cssText = 'font-weight:600;margin-bottom:8px;';
  if (result.classification === 'spam') {
    status.textContent = 'SPAM DETECTED';
    status.style.color = '#B00020';
  } else if (result.classification === 'not_spam') {
    status.textContent = 'NOT SPAM';
    status.style.color = '#0F9D58';
  } else {
    status.textContent = 'ANALYZED';
  }
  panel.appendChild(status);

  if (result.classification === 'spam' && result.ad) {
    const pre = document.createElement('pre');
    pre.style.cssText = 'white-space:pre-wrap;';
    pre.textContent = result.ad;
    panel.appendChild(pre);
  }

  const body = findMessageBody();
  if (body) {
    body.parentElement.insertBefore(panel, body.nextSibling);
  } else {
    document.body.appendChild(panel);
  }
}

function injectButton() {
  const body = findMessageBody();
  if (!body) return;
  if (document.getElementById('cyber-ad-btn')) return;
  const btn = createButton();
  btn.id = 'cyber-ad-btn';
  body.parentElement.insertBefore(btn, body);
}

// Observe DOM changes to re-inject when navigating emails
const observer = new MutationObserver(() => {
  injectButton();
});
observer.observe(document.body, { childList: true, subtree: true });

// Initial attempt
injectButton();
