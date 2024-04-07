console.log("Jai Swaminarayan")

function handleKeyPress(event) {
    if (event.key === 'Enter') {
        sendMessage();
    }
}

function sendMessage() {
    var messageInput = document.getElementById('message-input');
    var message = messageInput.value.trim();
    document.getElementById("send-button").disabled = true;

    if (message) {
        addMessageToChat(message, 'my-message');
        messageInput.value = '';
        fetch('http://localhost:5000/ask', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
            },
            body: JSON.stringify({question: message}),
        })
        .then(response => response.json())
        .then(data => {
            addMessageToChat('Incubyte: ' + data.response, 'response-message');
            document.getElementById("send-button").disabled = false;
        })
        .catch(error => {
            console.error('Error:', error);
            addMessageToChat('Incubyte: Sorry, there was an error processing your message.', 'error-message');
            document.getElementById("send-button").disabled = false;
        });
    }
}

function addMessageToChat(message, messageType) {
    var chatMessages = document.querySelector('.chat-messages');
    var messageElement = document.createElement('div');
    messageElement.classList.add(messageType);
    messageElement.textContent = message;

    var wrapperDiv = document.createElement('div');
    wrapperDiv.classList.add('message-wrapper');
    wrapperDiv.appendChild(messageElement);

    chatMessages.appendChild(wrapperDiv);
    chatMessages.scrollTop = chatMessages.scrollHeight; // Auto-scroll to the bottom
}