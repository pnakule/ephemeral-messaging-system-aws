// ── Character Counter ──────────────────────────────────────────────────────
const textarea = document.getElementById("message");
const counter  = document.getElementById("charCount");
const MAX      = 1000;

if (textarea && counter) {
  textarea.addEventListener("input", () => {
    const len = textarea.value.length;
    counter.textContent = `${len} / ${MAX}`;
    counter.classList.toggle("warn", len > MAX * 0.85);
  });
}

// ── Copy Link to Clipboard (FIXED) ─────────────────────────────────────────
function copyLink() {
  const linkEl  = document.getElementById("generatedLink");
  const copyBtn = document.getElementById("copyBtn");

  if (!linkEl || !copyBtn) return;

  const text = linkEl.textContent.trim();

  // Use modern clipboard only if available AND secure (HTTPS)
  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(text)
      .then(() => {
        copyBtn.textContent = "COPIED!";
        setTimeout(() => { copyBtn.textContent = "COPY LINK"; }, 2000);
      })
      .catch(() => fallbackCopy(text, linkEl, copyBtn));
  } else {
    fallbackCopy(text, linkEl, copyBtn);
  }
}

// Fallback method (works on HTTP)
function fallbackCopy(text, linkEl, copyBtn) {
  const range = document.createRange();
  range.selectNode(linkEl);
  window.getSelection().removeAllRanges();
  window.getSelection().addRange(range);

  try {
    document.execCommand("copy");
    copyBtn.textContent = "COPIED!";
  } catch (err) {
    copyBtn.textContent = "FAILED";
  }

  setTimeout(() => { copyBtn.textContent = "COPY LINK"; }, 2000);
}

// ── Countdown Timer (view page) ────────────────────────────────────────────
const destroyMsg = document.getElementById("destroyMsg");

if (destroyMsg) {
  let secs = 5;
  const interval = setInterval(() => {
    secs--;
    const el = document.getElementById("countdown");
    if (el) el.textContent = secs;
    if (secs <= 0) clearInterval(interval);
  }, 1000);
}
