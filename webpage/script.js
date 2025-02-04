const chatContainer = document.getElementById("chat");
const userInput = document.getElementById("userInput");

// Enviar mensaje con Enter
userInput.addEventListener("keypress", function(event) {
    if (event.key === "Enter") {
        sendMessage();
    }
});

// Enviar mensaje
async function sendMessage() {
    let message = userInput.value.trim();
    if (message === "") return;

    // Agregar mensaje del usuario al chat
    addMessage(message, "user-message");

    // Llamada a la API del chatbot
    try {
        let botReply = await fetchChatbotResponse(message);
        addMessage(botReply, "bot-message");
    } catch (error) {
        addMessage("Error retrieving response. Try again later.", "bot-message");
    }

    userInput.value = "";
}

// Agregar mensaje al chat
function addMessage(text, className) {
    let msgDiv = document.createElement("div");
    msgDiv.classList.add("message", className);
    msgDiv.textContent = text;
    chatContainer.appendChild(msgDiv);

    // Auto-scroll
    chatContainer.scrollTop = chatContainer.scrollHeight;
}

// Llamada a la API del chatbot en Python
async function fetchChatbotResponse(userText) {
    const apiUrl = "http://127.0.0.1:5000/chat";  // Cambiar si usas otro host

    const payload = {
        text: userText
    };

    const response = await fetch(apiUrl, {
        method: "POST",
        headers: {
            "Content-Type": "application/json"
        },
        body: JSON.stringify(payload)
    });

    if (!response.ok) {
        throw new Error("API error");
    }

    const data = await response.json();
    return data.reply || "I didn't understand that, but I'm learning. 😊";
}
