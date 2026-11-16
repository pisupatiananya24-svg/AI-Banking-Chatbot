const toggleButton = document.getElementById("chat-toggle");
const closeButton = document.getElementById("chat-close");
const chatPanel = document.getElementById("chat-panel");
const chatForm = document.getElementById("chat-form");
const chatInput = document.getElementById("chat-input");
const messages = document.getElementById("chat-messages");

toggleButton.addEventListener("click", () => chatPanel.classList.toggle("hidden"));
closeButton.addEventListener("click", () => chatPanel.classList.add("hidden"));

function addMessage(text, sender) {
  const message = document.createElement("div");
  message.className = `message ${sender}`;
  message.textContent = text;
  messages.appendChild(message);
  messages.scrollTop = messages.scrollHeight;
}

async function sendQuestion(question) {
  const cleanQuestion = question.trim();
  if (!cleanQuestion) return;

  addMessage(cleanQuestion, "user");
  chatInput.value = "";

  try {
    const response = await fetch("/chat", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ message: cleanQuestion })
    });
    const data = await response.json();
    addMessage(data.answer || "I couldn't process that question.", "bot");
  } catch (error) {
    addMessage("Unable to connect to the server. Please try again.", "bot");
  }
}

chatForm.addEventListener("submit", (event) => {
  event.preventDefault();
  sendQuestion(chatInput.value);
});

document.querySelectorAll(".quick-questions button").forEach((button) => {
  button.addEventListener("click", () => sendQuestion(button.dataset.question));
});
