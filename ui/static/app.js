const chatBox =
    document.getElementById("chat-box");

const traceBox =
    document.getElementById("tool-trace");

const input =
    document.getElementById("message-input");

const sendBtn =
    document.getElementById("send-btn");


// ======================================
// SEND MESSAGE
// ======================================

async function sendMessage() {

    const message =
        input.value.trim();

    if (!message)
        return;

    sendBtn.disabled = true;

    // ==================================
    // USER MESSAGE
    // ==================================

    chatBox.insertAdjacentHTML(
        "beforeend",
        `
        <div class="user-message">
            <b>You</b><br>
            ${escapeHtml(message)}
        </div>
        `
    );

    input.value = "";

    // ==================================
    // AGENT MESSAGE
    // ==================================

    const answerDiv =
        document.createElement("div");

    answerDiv.className =
        "answer";

    answerDiv.innerHTML = `
        <div class="agent-header">
            ⚽ Football Agent
        </div>

        <div class="agent-content">
            <span class="typing">
                Thinking...
            </span>
        </div>
    `;

    chatBox.appendChild(answerDiv);

    const answerContent =
        answerDiv.querySelector(
            ".agent-content"
        );

    scrollToBottom();

    // ==================================
    // TOOL TRACE RESET
    // ==================================

    traceBox.innerHTML = `
        <div class="tool">
            Waiting...
        </div>
    `;

    let currentAnswer = "";

    try {

        const response =
            await fetch(
                "/chat",
                {
                    method: "POST",

                    headers: {
                        "Content-Type":
                            "application/json"
                    },

                    body: JSON.stringify({
                        message,
                        thread_id: "demo"
                    })
                }
            );

        const reader =
            response.body.getReader();

        const decoder =
            new TextDecoder();

        let buffer = "";

        // ==================================
        // SSE LOOP
        // ==================================

        while (true) {

            const {
                done,
                value
            } = await reader.read();

            if (done)
                break;

            buffer += decoder.decode(
                value,
                {
                    stream: true
                }
            );

            const events =
                buffer.split("\n\n");

            buffer =
                events.pop();

            for (const eventText of events) {

                const line =
                    eventText
                        .split("\n")
                        .find(
                            l =>
                                l.startsWith("data:")
                        );

                if (!line)
                    continue;

                const event =
                    JSON.parse(
                        line.replace(
                            "data:",
                            ""
                        )
                    );

                console.log(event);

                // ==========================
                // TOOL START
                // ==========================

                if (
                    event.type ===
                    "tool_call"
                ) {

                    traceBox.insertAdjacentHTML(
                        "beforeend",
                        `
                        <div class="tool">
                            🔧 ${event.tool}
                        </div>
                        `
                    );

                    traceBox.scrollTop =
                        traceBox.scrollHeight;
                }

                // ==========================
                // TOOL END
                // ==========================

                else if (
                    event.type ===
                    "tool_result"
                ) {

                    if (!event.tool)
                        continue;

                    traceBox.insertAdjacentHTML(
                        "beforeend",
                        `
                        <div class="tool-result">
                            ✅ ${event.tool}
                        </div>
                        `
                    );
                }

                // ==========================
                // TOKEN
                // ==========================

                else if (
                    event.type ===
                    "token"
                ) {

                    currentAnswer +=
                        event.content;

                    answerContent.textContent =
                        currentAnswer;

                    scrollToBottom();
                }

                else if (
                    event.type ===
                    "answer"
                ) {

                    currentAnswer =
                        event.content;

                    answerContent.innerHTML =
                        marked.parse(
                            currentAnswer
                        );

                    scrollToBottom();
                }
                // ==========================
                // DONE
                // ==========================

                else if (
                    event.type ===
                    "done"
                ) {

                    answerContent.innerHTML =
                        marked.parse(
                            currentAnswer
                        );

                    scrollToBottom();
                }
            }
        }

    } catch (err) {

        answerContent.innerHTML = `
            <div class="error">
                Error: ${err}
            </div>
        `;

        console.error(err);

    } finally {

        sendBtn.disabled = false;
        input.focus();
    }
}


// ======================================
// ENTER TO SEND
// ======================================

input.addEventListener(
    "keydown",
    (e) => {

        if (
            e.key === "Enter" &&
            !e.shiftKey
        ) {

            e.preventDefault();

            sendMessage();
        }
    }
);


// ======================================
// HELPERS
// ======================================

function scrollToBottom() {

    chatBox.scrollTop =
        chatBox.scrollHeight;
}


function escapeHtml(text) {

    const div =
        document.createElement("div");

    div.textContent = text;

    return div.innerHTML;
}