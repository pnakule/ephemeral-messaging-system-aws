// ── Char Counter ──────────────────────────────────────────────
const textarea = document.getElementById("message");
const counter  = document.getElementById("charCount");
const MAX      = 1000;

if (textarea && counter) {
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

  // Works for both input and text elements
  const text = linkEl.value || linkEl.textContent.trim();

  if (!text) return;

  // Modern method
  if (navigator.clipboard && window.isSecureContext) {
    navigator.clipboard.writeText(text)
      .then(() => showCopied(copyBtn))
      .catch(() => fallbackCopy(text, copyBtn));
  } else {
    // Fallback if clipboard API not available
    fallbackCopy(text, copyBtn);
  }
}

// ── Fallback Copy (reliable) ──────────────────────────────────
function fallbackCopy(text, btn) {
  const tempInput = document.createElement("input");
  tempInput.value = text;
  document.body.appendChild(tempInput);
  tempInput.select();
  tempInput.setSelectionRange(0, 99999); // mobile support
  document.execCommand("copy");
  document.body.removeChild(tempInput);

  showCopied(btn);
}

// ── Helper ────────────────────────────────────────────────────
function showCopied(btn) {
  const original = btn.textContent;
  btn.textContent = "Copied!";
  setTimeout(() => {
    btn.textContent = original;
  }, 2000);
}}, 2000);
}
