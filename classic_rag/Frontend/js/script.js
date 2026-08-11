// ============================================================
// CONFIG
// ============================================================

const API_URL = "http://localhost:8002/query";


// ============================================================
// AUTO RESIZE TEXTAREA
// ============================================================

function autoResize(el) {
    el.style.height = "auto";
    el.style.height = Math.min(el.scrollHeight, 140) + "px";
}


// ============================================================
// SAMPLE QUESTION CLICK
// ============================================================

function setQuery(el) {
    const input = document.getElementById("queryInput");

    input.value = el.textContent;

    autoResize(input);

    input.focus();
}


// ============================================================
// ENTER KEY HANDLER
// Enter      → Send
// Shift+Enter → New line
// ============================================================

function handleKey(e) {

    if (e.key === "Enter" && !e.shiftKey) {

        e.preventDefault();

        sendQuery();
    }
}


// ============================================================
// REMOVE EMPTY STATE
// ============================================================

function removeEmpty() {

    const empty = document.getElementById("emptyState");

    if (empty) {
        empty.remove();
    }
}


// ============================================================
// SCROLL TO BOTTOM
// ============================================================

function scrollBottom() {

    const msgs = document.getElementById("messages");

    if (msgs) {
        msgs.scrollTop = msgs.scrollHeight;
    }
}


// ============================================================
// ADD USER MESSAGE
// ============================================================

function addUserMsg(text) {

    removeEmpty();

    const msgs = document.getElementById("messages");

    const div = document.createElement("div");

    div.className = "msg user";

    div.innerHTML = `
        <div class="avatar user">👤</div>

        <div class="bubble">
            ${escHtml(text)}
        </div>
    `;

    msgs.appendChild(div);

    scrollBottom();
}


// ============================================================
// ADD THINKING INDICATOR
// ============================================================

function addThinking() {

    const msgs = document.getElementById("messages");

    // Avoid duplicate thinking indicators
    removeThinking();

    const div = document.createElement("div");

    div.className = "thinking";

    div.id = "thinking";

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


// ============================================================
// REMOVE THINKING INDICATOR
// ============================================================

function removeThinking() {

    const thinking = document.getElementById("thinking");

    if (thinking) {
        thinking.remove();
    }
}


// ============================================================
// ADD AI ANSWER
// ============================================================

function addAIMsg(data) {

    const msgs = document.getElementById("messages");

    const div = document.createElement("div");

    div.className = "msg";


// ============================================================
// BUILD SOURCES
// ============================================================

    let sourcesHtml = "";

    if (
        data.sources &&
        Array.isArray(data.sources) &&
        data.sources.length > 0
    ) {

        const chips = data.sources.map(source => {

            const isImage =
                source.type &&
                source.type.toLowerCase() === "image";

            return `
                <div class="source-chip ${isImage ? "chip-type-image" : ""}">

                    <span class="chip-icon">
                        ${isImage ? "🖼" : "📄"}
                    </span>

                    Page ${escHtml(String(source.page))}

                    ·

                    ${escHtml(String(source.type))}

                </div>
            `;

        }).join("");


        sourcesHtml = `
            <div class="sources-wrap">

                <div class="sources-label">
                    Sources retrieved
                </div>

                <div class="sources-list">
                    ${chips}
                </div>

            </div>
        `;
    }


// ============================================================
// BUILD RETRIEVED CHUNKS
// ============================================================

    let chunksHtml = "";

    if (
        data.retrieved_chunks &&
        Array.isArray(data.retrieved_chunks) &&
        data.retrieved_chunks.length > 0
    ) {

        const chunkId = "chunks_" + Date.now();

        const items = data.retrieved_chunks.map((chunk, index) => {

            return `
                <div class="chunk-item">

                    <div class="chunk-header">

                        <span>
                            Chunk ${index + 1}

                            · Page ${escHtml(String(chunk.page))}

                            · ${escHtml(String(chunk.type))}
                        </span>

                    </div>

                    <div class="chunk-content">

                        ${escHtml(String(chunk.content || ""))}

                    </div>

                </div>
            `;

        }).join("");


        chunksHtml = `
            <button
                class="chunks-toggle"
                onclick="toggleChunks('${chunkId}')"
            >
                ▶ Show retrieved chunks
            </button>

            <div
                class="chunks-list"
                id="${chunkId}"
                style="display:none"
            >
                ${items}
            </div>
        `;
    }


// ============================================================
// FINAL AI MESSAGE
// ============================================================

    div.innerHTML = `

        <div class="avatar ai">
            🤖
        </div>

        <div class="bubble">

            ${formatAnswer(data.answer || "No answer returned.")}

            ${sourcesHtml}

            ${chunksHtml}

        </div>
    `;


    msgs.appendChild(div);

    scrollBottom();
}


// ============================================================
// ADD ERROR MESSAGE
// ============================================================

function addError(message) {

    const msgs = document.getElementById("messages");

    const div = document.createElement("div");

    div.className = "msg";

    div.innerHTML = `

        <div class="avatar ai">
            🤖
        </div>

        <div class="error-bubble">

            ⚠️ ${escHtml(message)}

        </div>
    `;

    msgs.appendChild(div);

    scrollBottom();
}


// ============================================================
// TOGGLE RETRIEVED CHUNKS
// ============================================================

function toggleChunks(id) {

    const element = document.getElementById(id);

    if (!element) {
        return;
    }

    const button = element.previousElementSibling;


    if (element.style.display === "none") {

        element.style.display = "flex";

        if (button) {
            button.textContent = "▼ Hide retrieved chunks";
        }

    } else {

        element.style.display = "none";

        if (button) {
            button.textContent = "▶ Show retrieved chunks";
        }
    }
}


// ============================================================
// FORMAT ANSWER
// ============================================================

function formatAnswer(text) {

    if (!text) {
        return "";
    }

    return escHtml(String(text))

        // Markdown bold
        .replace(
            /\*\*(.*?)\*\*/g,
            "<strong>$1</strong>"
        )

        // New lines
        .replace(
            /\n\n/g,
            "<br><br>"
        )

        .replace(
            /\n/g,
            "<br>"
        );
}


// ============================================================
// ESCAPE HTML
// Prevent HTML injection
// ============================================================

function escHtml(value) {

    if (value === null || value === undefined) {
        return "";
    }

    const div = document.createElement("div");

    div.textContent = String(value);

    return div.innerHTML;
}


// ============================================================
// MAIN SEND QUERY FUNCTION
// ============================================================

async function sendQuery() {

    const input = document.getElementById("queryInput");

    const sendBtn = document.getElementById("sendBtn");


    if (!input) {

        console.error("queryInput element not found");

        return;
    }


    const question = input.value.trim();


    // Don't send empty question
    if (!question) {
        return;
    }


    // Disable button
    if (sendBtn) {
        sendBtn.disabled = true;
    }


    // Clear input
    input.value = "";

    autoResize(input);


    // Add user message
    addUserMsg(question);


    // Add thinking animation
    addThinking();


    try {

        console.log("Sending request to:", API_URL);

        console.log("Question:", question);


        // ====================================================
        // CALL FASTAPI
        // ====================================================

        const response = await fetch(API_URL, {

            method: "POST",

            headers: {
                "Content-Type": "application/json"
            },

            body: JSON.stringify({
                question: question
            })

        });


        // Remove thinking indicator
        removeThinking();


        // ====================================================
        // CHECK HTTP RESPONSE
        // ====================================================

        if (!response.ok) {

            let errorMessage =
                `API error ${response.status}`;

            try {

                const errorData = await response.json();

                if (errorData.detail) {
                    errorMessage += ` — ${errorData.detail}`;
                }

            } catch (e) {

                // Response wasn't JSON
            }


            addError(errorMessage);

            return;
        }


        // ====================================================
        // CONVERT RESPONSE TO JSON
        // ====================================================

        const data = await response.json();


        console.log("FastAPI response:", data);


        // ====================================================
        // VALIDATE RESPONSE
        // ====================================================

        if (!data) {

            addError("Empty response received from FastAPI.");

            return;
        }


        // ====================================================
        // DISPLAY AI RESPONSE
        // ====================================================

        addAIMsg(data);


    } catch (error) {

        console.error("Fetch error:", error);


        removeThinking();


        addError(
            "Cannot connect to FastAPI. " +
            "Make sure your server is running on " +
            "http://localhost:8002"
        );


    } finally {

        // Enable button
        if (sendBtn) {
            sendBtn.disabled = false;
        }


        // Put cursor back into input
        input.focus();
    }
}
