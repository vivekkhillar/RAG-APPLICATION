// ── config ──
const API_URL = 'http://localhost:8000/query';
 
// ── auto resize textarea ──
function autoResize(el) {
  el.style.height = 'auto';
  el.style.height = Math.min(el.scrollHeight, 140) + 'px';
}

// ── sample question click ──
function setQuery(el) {
  const input = document.getElementById('queryInput');
  input.value = el.textContent;
  autoResize(input);
  input.focus();
}

// ── enter key handler ──
function handleKey(e) {
  if (e.key === 'Enter' && !e.shiftKey) {
    e.preventDefault();
    sendQuery();
  }
}

// ── remove empty state ──
function removeEmpty() {
  const empty = document.getElementById('emptyState');
  if (empty) empty.remove();
}

// ── scroll to bottom ──
function scrollBottom() {
  const msgs = document.getElementById('messages');
  msgs.scrollTop = msgs.scrollHeight;
}

// ── add user message ──
function addUserMsg(text) {
  removeEmpty();
  const msgs = document.getElementById('messages');
  const div = document.createElement('div');
  div.className = 'msg user';
  div.innerHTML = `
    <div class="avatar user">👤</div>
    <div class="bubble">${escHtml(text)}</div>
  `;
  msgs.appendChild(div);
  scrollBottom();
}

// ── add thinking indicator ──
function addThinking() {
  const msgs = document.getElementById('messages');
  const div = document.createElement('div');
  div.className = 'thinking';
  div.id = 'thinking';
  div.innerHTML = `
    <div class="avatar ai">🤖</div>
    <div class="think-bubble">
      <div class="dots">
        <div class="dot"></div>
        <div class="dot"></div>
        <div class="dot"></div>
      </div>
      Searching document and generating answer...
    </div>
  `;
  msgs.appendChild(div);
  scrollBottom();
}

// ── remove thinking indicator ──
function removeThinking() {
  const t = document.getElementById('thinking');
  if (t) t.remove();
}

// ── add AI answer ──
function addAIMsg(data) {
  const msgs = document.getElementById('messages');
  const div = document.createElement('div');
  div.className = 'msg';

  // build sources chips
  let sourcesHtml = '';
  if (data.sources && data.sources.length > 0) {
    const chips = data.sources.map(s => {
      const isImage = s.type === 'image' || s.type === 'Image';
      return `
        <div class="source-chip ${isImage ? 'chip-type-image' : ''}">
          <span class="chip-icon">${isImage ? '🖼' : '📄'}</span>
          Page ${s.page} · ${s.type}
        </div>
      `;
    }).join('');

    sourcesHtml = `
      <div class="sources-wrap">
        <div class="sources-label">Sources retrieved</div>
        <div class="sources-list">${chips}</div>
      </div>
    `;
  }

  // build chunks toggle (if retrieved_chunks present)
  let chunksHtml = '';
  if (data.retrieved_chunks && data.retrieved_chunks.length > 0) {
    const chunkId = 'chunks_' + Date.now();
    const items = data.retrieved_chunks.map((c, i) => `
      <div class="chunk-item">
        <div class="chunk-header">
          <span>Chunk ${i+1} · Page ${c.page} · ${c.type}</span>
        </div>
        ${escHtml(c.content)}...
      </div>
    `).join('');

    chunksHtml = `
      <button class="chunks-toggle" onclick="toggleChunks('${chunkId}')">
        ▶ Show retrieved chunks
      </button>
      <div class="chunks-list" id="${chunkId}" style="display:none">
        ${items}
      </div>
    `;
  }

  div.innerHTML = `
    <div class="avatar ai">🤖</div>
    <div class="bubble">
      ${formatAnswer(data.answer)}
      ${sourcesHtml}
      ${chunksHtml}
    </div>
  `;

  msgs.appendChild(div);
  scrollBottom();
}

// ── add error message ──
function addError(msg) {
  const msgs = document.getElementById('messages');
  const div = document.createElement('div');
  div.className = 'msg';
  div.innerHTML = `
    <div class="avatar ai">🤖</div>
    <div class="error-bubble">⚠️ ${escHtml(msg)}</div>
  `;
  msgs.appendChild(div);
  scrollBottom();
}

// ── toggle chunks visibility ──
function toggleChunks(id) {
  const el  = document.getElementById(id);
  const btn = el.previousElementSibling;
  if (el.style.display === 'none') {
    el.style.display = 'flex';
    btn.textContent  = '▼ Hide retrieved chunks';
  } else {
    el.style.display = 'none';
    btn.textContent  = '▶ Show retrieved chunks';
  }
}

// ── format answer text ──
function formatAnswer(text) {
  return escHtml(text)
    .replace(/\n\n/g, '</p><p style="margin-top:10px">')
    .replace(/\n/g,   '<br>')
    .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
    .replace(/•\s/g,  '• ');
}

// ── escape html ──
function escHtml(str) {
  const d = document.createElement('div');
  d.textContent = str;
  return d.innerHTML;
}

// ── main send function ──
async function sendQuery() {
  const input   = document.getElementById('queryInput');
  const sendBtn = document.getElementById('sendBtn');
  const question = input.value.trim();

  if (!question) return;

  // clear input
  input.value = '';
  autoResize(input);
  sendBtn.disabled = true;

  // show user message + thinking
  addUserMsg(question);
  addThinking();

  try {
    const response = await fetch(API_URL, {
      method : 'POST',
      headers: { 'Content-Type': 'application/json' },
      body   : JSON.stringify({ question })
    });

    removeThinking();

    if (!response.ok) {
      addError(`API error ${response.status} — check your FastAPI server is running on port 8000`);
      return;
    }

    const data = await response.json();
    addAIMsg(data);

  } catch (err) {
    removeThinking();
    addError('Cannot connect to API — make sure FastAPI is running on http://localhost:8000');
  } finally {
    sendBtn.disabled = false;
    input.focus();
  }
}