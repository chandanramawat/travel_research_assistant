// ---------------------------------------------------------------------------
// Config
// ---------------------------------------------------------------------------
const BACKEND_URL = "http://localhost:8000/ask";

// Session id: kept in memory only for this page load (no localStorage —
// matches a fresh Streamlit session each time you reload the page).
const sessionId = crypto.randomUUID();

const TAG_HTML = {
  weather: '<span class="tag tag-weather">Weather Tool</span>',
  research: '<span class="tag tag-research">Tavily Search</span>',
  itinerary: '<span class="tag tag-itinerary">Itinerary Planner</span>',
  none: '<span class="tag tag-none">Direct LLM</span>',
};

// ---------------------------------------------------------------------------
// DOM refs
// ---------------------------------------------------------------------------
const chatMessages = document.getElementById("chatMessages");
const chatInput = document.getElementById("chatInput");
const sendBtn = document.getElementById("sendBtn");
const sidebar = document.getElementById("sidebar");
const sidebarToggle = document.getElementById("sidebarToggle");

// ---------------------------------------------------------------------------
// Helpers
// ---------------------------------------------------------------------------
function escapeHtml(str) {
  const div = document.createElement("div");
  div.textContent = str;
  return div.innerHTML;
}

function addMessage(role, text, toolUsed) {
  const msg = document.createElement("div");
  msg.className = `msg ${role}`;

  const avatar = document.createElement("div");
  avatar.className = "msg-avatar";
  avatar.textContent = role === "user" ? "U" : "✦";

  const body = document.createElement("div");
  body.className = "msg-body";

  const textEl = document.createElement("div");
  textEl.className = "msg-text";
  textEl.textContent = text;
  body.appendChild(textEl);

  if (role === "assistant") {
    const tagWrap = document.createElement("div");
    tagWrap.innerHTML = TAG_HTML[toolUsed] || TAG_HTML.none;
    body.appendChild(tagWrap);
  }

  msg.appendChild(avatar);
  msg.appendChild(body);
  chatMessages.appendChild(msg);
  chatMessages.scrollTop = chatMessages.scrollHeight;
  return msg;
}

function addThinkingIndicator() {
  const msg = document.createElement("div");
  msg.className = "msg assistant";
  msg.id = "thinkingMsg";

  const avatar = document.createElement("div");
  avatar.className = "msg-avatar";
  avatar.textContent = "✦";

  const body = document.createElement("div");
  body.className = "msg-body thinking";
  body.innerHTML = `Thinking <span class="dot-flash"><span></span><span></span><span></span></span>`;

  msg.appendChild(avatar);
  msg.appendChild(body);
  chatMessages.appendChild(msg);
  chatMessages.scrollTop = chatMessages.scrollHeight;
}

function removeThinkingIndicator() {
  const el = document.getElementById("thinkingMsg");
  if (el) el.remove();
}

// ---------------------------------------------------------------------------
// Core send flow
// ---------------------------------------------------------------------------
async function sendMessage(text) {
  const trimmed = text.trim();
  if (!trimmed) return;

  addMessage("user", trimmed);
  chatInput.value = "";
  sendBtn.disabled = true;
  addThinkingIndicator();

  const controller = new AbortController();
  const timeout = setTimeout(() => controller.abort(), 60000); // 60s timeout

  try {
    const res = await fetch(BACKEND_URL, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: trimmed, session_id: sessionId }),
      signal: controller.signal,
    });

    clearTimeout(timeout);
    const data = await res.json();
    const answer = data.response || "No response";
    const toolUsed = data.tool_used || "none";

    removeThinkingIndicator();
    addMessage("assistant", answer, toolUsed);
  } catch (err) {
    clearTimeout(timeout);
    removeThinkingIndicator();
    const message = err.name === "AbortError" ? "Timeout error" : "Something went wrong!";
    addMessage("assistant", message, "none");
  } finally {
    sendBtn.disabled = false;
    chatInput.focus();
  }
}

// ---------------------------------------------------------------------------
// Event listeners
// ---------------------------------------------------------------------------
sendBtn.addEventListener("click", () => sendMessage(chatInput.value));

chatInput.addEventListener("keydown", (e) => {
  if (e.key === "Enter" && !e.shiftKey) {
    e.preventDefault();
    sendMessage(chatInput.value);
  }
});

document.querySelectorAll(".suggest-btn").forEach((btn) => {
  btn.addEventListener("click", () => {
    sendMessage(btn.dataset.suggestion);
    sidebar.classList.remove("open"); // close on mobile after picking
  });
});

sidebarToggle.addEventListener("click", () => {
  sidebar.classList.toggle("open");
});