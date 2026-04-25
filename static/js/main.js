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

// ── Copy Link to Clipboard ─────────────────────────────────────────────────
function copyLink() {
  const linkEl  = document.getElementById("generatedLink");
  const copyBtn = document.getElementById("copyBtn");

  if (!linkEl || !copyBtn) return;

  navigator.clipboard.writeText(linkEl.textContent.trim())
    .then(() => {
      copyBtn.textContent = "COPIED!";
      setTimeout(() => { copyBtn.textContent = "COPY LINK"; }, 2000);
    })
    .catch(() => {
      // fallback for older browsers
      const range = document.createRange();
      range.selectNode(linkEl);
      window.getSelection().removeAllRanges();
      window.getSelection().addRange(range);
      document.execCommand("copy");
      copyBtn.textContent = "COPIED!";
      setTimeout(() => { copyBtn.textContent = "COPY LINK"; }, 2000);
    });
}

// ── Countdown Timer (view page) ────────────────────────────────────────────
// Shows user a "this message was just destroyed" feel after reading
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
