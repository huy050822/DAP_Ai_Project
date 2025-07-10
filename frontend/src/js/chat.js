let chatHistory = [];
const API_URL = 'http://localhost:8000';

document.addEventListener('DOMContentLoaded', function() {
    const chatMessages = document.querySelector('.chat-messages');
    const chatInput = document.querySelector('.chat-input textarea');
    const sendButton = document.querySelector('.send-btn');
    const chatHistoryContainer = document.querySelector('.chat-history');
    const productList = document.querySelector('.product-list');
    const newChatBtn = document.querySelector('.new-chat-btn');

    // Auto-resize textarea
    chatInput.addEventListener('input', function() {
        this.style.height = 'auto';
        this.style.height = (this.scrollHeight) + 'px';
    });

    // Format analysis results for display
    function formatAnalysisResult(content) {
        if (!content) return '';

        // Làm nổi bật tên sản phẩm trong danh sách top sản phẩm
        let lines = content.split('\n');
        lines = lines.map(line => {
            // Nếu là dòng số thứ tự sản phẩm (ví dụ: 1. Tên sản phẩm)
            const match = line.match(/^([0-9]+)\. (.+)$/);
            if (match) {
                // Thêm class product-name-highlight và badge nếu là top 1
                let badge = '';
                if (match[1] === '1') badge = ' <span class="product-badge">Best Seller</span>';
                return `<span class="product-name-highlight">${match[1]}. ${match[2]}</span>${badge}`;
            }
            if (line.startsWith('•')) {
                return `<div class="analysis-point">${line}</div>`;
            } else if (line.startsWith('-')) {
                return `<div class="analysis-detail">${line}</div>`;
            }
            return line;
        });
        return lines.join('<br>');
    }

    // Add message to chat
    function appendMessage(content, type = 'user', messageType = 'text') {
        const messageDiv = document.createElement('div');
        messageDiv.className = `message ${type}`;
        
        const contentDiv = document.createElement('div');
        contentDiv.className = 'message-content';
        
        if (type === 'user') {
            contentDiv.textContent = content;
        } else {
            contentDiv.innerHTML = messageType === 'analysis' ? 
                formatAnalysisResult(content) : 
                content.replace(/\n/g, '<br>');
        }
        
        messageDiv.appendChild(contentDiv);
        chatMessages.appendChild(messageDiv);
        chatMessages.scrollTop = chatMessages.scrollHeight;

        // Add to history if it's an assistant message
        if (type === 'assistant') {
            addToHistory(content);
        }
    }

    // Add to chat history
    function addToHistory(content) {
        const historyItem = document.createElement('div');
        historyItem.className = 'history-item';
        const title = content.split('\n')[0];
        historyItem.innerHTML = `
            <div class="history-title">${title.substring(0, 30)}...</div>
            <div class="history-time">${new Date().toLocaleTimeString()}</div>
        `;
        chatHistoryContainer.insertBefore(historyItem, chatHistoryContainer.firstChild);

        // Add click event to load this conversation
        historyItem.addEventListener('click', () => {
            chatInput.value = title;
            sendMessage();
        });
    }

    // Update product suggestions
    function updateProductSuggestions(products) {
        if (!productList) return;
        
        productList.innerHTML = products.map(product => `
            <div class="product-card">
                <div class="product-name">${product.product_name}</div>
                <div class="product-price">$${product.sales_per_order.toLocaleString()}</div>
                <div class="product-stats">
                    <span>Quantity: ${product.order_quantity}</span>
                </div>
            </div>
        `).join('');
    }

    // Send message function
    async function sendMessage() {
        const message = chatInput.value.trim();
        if (!message) return;

        // Clear input and reset height
        chatInput.value = '';
        chatInput.style.height = 'auto';
        
        // Add user message
        appendMessage(message, 'user');

        // Show typing indicator
        const loadingDiv = document.createElement('div');
        loadingDiv.className = 'message assistant loading';
        loadingDiv.innerHTML = '<div class="message-content"><div class="typing-indicator"><span></span><span></span><span></span></div></div>';
        chatMessages.appendChild(loadingDiv);

        try {
            const response = await fetch('/api/forecast/chat/message', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({
                    user_id: 'demo',
                    message: message
                })
            });

            const data = await response.json();
            loadingDiv.remove();

            if (data.status === 'success') {
                appendMessage(data.response, 'assistant', 'analysis');
                
                // Update product suggestions if available
                if (data.analysis_results?.top_products) {
                    updateProductSuggestions(data.analysis_results.top_products);
                }
            } else {
                throw new Error('Invalid response format');
            }
        } catch (error) {
            console.error('Error:', error);
            loadingDiv.remove();
            appendMessage('Xin lỗi, đã có lỗi xảy ra. Vui lòng thử lại sau.', 'assistant');
        }
    }

    // Event listeners
    chatInput.addEventListener('keypress', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            sendMessage();
        }
    });

    sendButton.addEventListener('click', sendMessage);

    newChatBtn.addEventListener('click', () => {
        chatMessages.innerHTML = '';
        showWelcomeMessage();
    });

    // Show welcome message
    function showWelcomeMessage() {
        appendMessage(`Xin chào! Tôi là trợ lý AI, tôi có thể giúp bạn phân tích:

• Sản phẩm bán chạy nhất
• Phân tích khách hàng
• Tình trạng giao hàng
• Dự báo xu hướng

Bạn muốn biết thông tin gì?`, 'assistant', 'analysis');
    }

    // Initialize
    showWelcomeMessage();
});
