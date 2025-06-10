// Initialize WebSocket connection
const socket = io('http://localhost:8000');
let chatHistory = [];

document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.querySelector('.chat-messages');
    const chatInput = document.querySelector('.chat-input textarea');
    const sendButton = document.querySelector('.send-btn');
    const newChatBtn = document.querySelector('.new-chat-btn');
    const chatHistoryContainer = document.querySelector('.chat-history');
    const productList = document.querySelector('.product-list');

    // Handle send message
    function sendMessage() {
        const message = chatInput.value.trim();
        if (message) {
            // Add user message to chat
            addMessage(message, 'user');
            
            // Send message to server
            socket.emit('chat_message', {
                message: message,
                timestamp: new Date().toISOString()
            });

            // Clear input
            chatInput.value = '';
            
            // Show typing indicator
            showTypingIndicator();
        }
    }

    // Add message to chat
    function addMessage(message, type, products = []) {
        const messageDiv = document.createElement('div');
        messageDiv.classList.add('message', `${type}-message`);
        messageDiv.textContent = message;
        chatMessages.appendChild(messageDiv);
        
        // If there are product suggestions, update the product list
        if (products.length > 0) {
            updateProductSuggestions(products);
        }

        // Scroll to bottom
        chatMessages.scrollTop = chatMessages.scrollHeight;

        // Add to chat history
        chatHistory.push({
            type,
            message,
            timestamp: new Date().toISOString()
        });

        // Update chat history sidebar
        updateChatHistory();
    }

    // Show AI is typing indicator
    function showTypingIndicator() {
        const indicator = document.createElement('div');
        indicator.classList.add('message', 'ai-message', 'typing-indicator');
        indicator.textContent = 'AI is typing...';
        chatMessages.appendChild(indicator);
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }

    // Update product suggestions
    function updateProductSuggestions(products) {
        productList.innerHTML = '';
        products.forEach(product => {
            const productCard = document.createElement('div');
            productCard.classList.add('product-card');
            productCard.innerHTML = `
                <img src="${product.image}" alt="${product.name}">
                <h4>${product.name}</h4>
                <p>${product.description}</p>
                <span class="price">$${product.price}</span>
            `;
            productList.appendChild(productCard);
        });
    }

    // Update chat history sidebar
    function updateChatHistory() {
        chatHistoryContainer.innerHTML = '';
        const groupedHistory = groupChatsByDate(chatHistory);
        
        Object.entries(groupedHistory).forEach(([date, messages]) => {
            const historyItem = document.createElement('div');
            historyItem.classList.add('history-item');
            historyItem.innerHTML = `
                <div class="history-date">${formatDate(date)}</div>
                <div class="history-preview">${messages[0].message.substring(0, 30)}...</div>
            `;
            chatHistoryContainer.appendChild(historyItem);
        });
    }

    // Group chats by date
    function groupChatsByDate(history) {
        return history.reduce((groups, item) => {
            const date = new Date(item.timestamp).toLocaleDateString();
            if (!groups[date]) {
                groups[date] = [];
            }
            groups[date].push(item);
            return groups;
        }, {});
    }

    // Format date
    function formatDate(dateString) {
        const date = new Date(dateString);
        return new Intl.DateTimeFormat('en-US', {
            month: 'short',
            day: 'numeric'
        }).format(date);
    }

    // Event Listeners
    sendButton.addEventListener('click', sendMessage);
    
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    newChatBtn.addEventListener('click', () => {
        chatMessages.innerHTML = '';
        chatHistory = [];
        updateChatHistory();
        
        // Add welcome message
        const welcomeDiv = document.createElement('div');
        welcomeDiv.classList.add('welcome-message');
        welcomeDiv.innerHTML = `
            <h2>How can I help you today?</h2>
            <p>Ask me about product recommendations, pricing, or any other questions about our products!</p>
        `;
        chatMessages.appendChild(welcomeDiv);
    });

    // Socket event handlers
    socket.on('ai_response', (data) => {
        // Remove typing indicator
        const typingIndicator = document.querySelector('.typing-indicator');
        if (typingIndicator) {
            typingIndicator.remove();
        }

        // Add AI response
        addMessage(data.message, 'ai', data.products || []);
    });

    socket.on('error', (error) => {
        console.error('Socket error:', error);
        addMessage('Sorry, there was an error processing your request. Please try again.', 'ai');
    });
});
