// ── Char Counter ──────────────────────────────────────────────
const textarea = document.getElementById("message");
const counter  = document.getElementById("charCount");
const MAX      = 1000;

if (textarea && counter) {
  // Initialize on page load
  counter.textContent = `0 / ${MAX}`;

  textarea.addEventListener("input", () => {
    const len = textarea.value.length;
    counter.textContent = `${len} / ${MAX}`;
    counter.classList.toggle("warn", len > MAX * 0.85);
  });
}

// ── Copy Link ─────────────────────────────────────────────────
function copyLink() {
  const linkEl  = document.getElementById("generatedLink");
  const copyBtn = document.getElementById("copyBtn");

  if (!linkEl || !copyBtn) return;

  const text = linkEl.textContent.trim();

  navigator.clipboard.writeText(text)
    .then(() => {
      showCopied(copyBtn);
    })
    .catch(() => {
      // Fallback for older browsers
      const range = document.createRange();
      range.selectNode(linkEl);
      window.getSelection().removeAllRanges();
      window.getSelection().addRange(range);
      document.execCommand("copy");
      window.getSelection().removeAllRanges();

      showCopied(copyBtn);
    });
}

// ── Helper ────────────────────────────────────────────────────
function showCopied(btn) {
  btn.textContent = "Copied!";
  setTimeout(() => {
    btn.textContent = "Copy Link";
  }, 2000);
}
