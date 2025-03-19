document.addEventListener('DOMContentLoaded', () => {
    // Основные элементы интерфейса
    const chatForm = document.getElementById('chatForm');
    const userInput = document.getElementById('userInput');
    const chatMessages = document.getElementById('chatMessages');
    const sendButton = document.getElementById('sendButton');
    const clearChatButton = document.getElementById('clearChat');
    
    // Автоматическое изменение высоты текстового поля
    userInput.addEventListener('input', () => {
        // Сброс высоты перед расчетом
        userInput.style.height = 'auto';
        // Установка высоты на основе содержимого
        userInput.style.height = (userInput.scrollHeight) + 'px';
        
        // Активация/деактивация кнопки отправки
        sendButton.disabled = userInput.value.trim() === '';
    });
    
    // Отправка сообщения по нажатию Enter (без Shift)
    userInput.addEventListener('keydown', (e) => {
        if (e.key === 'Enter' && !e.shiftKey) {
            e.preventDefault();
            
            if (userInput.value.trim() !== '') {
                chatForm.dispatchEvent(new Event('submit'));
            }
        }
    });
    
    // Обработка отправки формы
    chatForm.addEventListener('submit', async (e) => {
        e.preventDefault();
        
        const message = userInput.value.trim();
        if (message === '') return;
        
        // Добавление сообщения пользователя в чат
        addMessage(message, 'user');
        
        // Очистка поля ввода
        userInput.value = '';
        userInput.style.height = 'auto';
        sendButton.disabled = true;
        
        // Показываем индикатор загрузки
        showTypingIndicator();
        
        try {
            // Отправка сообщения на сервер
            const response = await fetch('/api/chat', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                },
                body: JSON.stringify({ message }),
            });
            
            const data = await response.json();
            
            // Удаляем индикатор загрузки
            removeTypingIndicator();
            
            if (response.ok && data.success) {
                // Добавление ответа ассистента
                addMessage(data.message, 'assistant');
            } else {
                // Обработка ошибки
                console.error('Ошибка при получении ответа:', data.error || 'Неизвестная ошибка');
                addMessage('Извините, произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте еще раз.', 'assistant', true);
            }
        } catch (error) {
            // Удаляем индикатор загрузки
            removeTypingIndicator();
            console.error('Ошибка при отправке запроса:', error);
            addMessage('Извините, не удалось подключиться к серверу. Пожалуйста, проверьте соединение и попробуйте снова.', 'assistant', true);
        }
        
        // Прокрутка чата вниз
        scrollToBottom();
    });
    
    // Очистка чата
    clearChatButton.addEventListener('click', async () => {
        // Запрос на сервер для очистки истории
        try {
            const response = await fetch('/api/clear_history', {
                method: 'POST',
            });
            
            if (response.ok) {
                // Очистка UI чата (кроме приветственного сообщения)
                chatMessages.innerHTML = `
                    <div class="message assistant">
                        <div class="message-content">
                            <div class="message-bubble">
                                <p>Привет! Я Кэролайн, ваш ассистент. Чем я могу помочь вам сегодня?</p>
                            </div>
                        </div>
                    </div>
                `;
            }
        } catch (error) {
            console.error('Ошибка при очистке истории:', error);
        }
    });
    
    // Функция добавления сообщения в чат
    function addMessage(content, sender, isError = false) {
        const messageElement = document.createElement('div');
        messageElement.className = `message ${sender}`;
        
        let formattedContent = content;
        
        // Обработка переносов строк
        formattedContent = formattedContent.replace(/\n/g, '<br>');
        
        messageElement.innerHTML = `
            <div class="message-content">
                <div class="message-bubble ${isError ? 'error' : ''}">
                    <p>${formattedContent}</p>
                </div>
            </div>
        `;
        
        chatMessages.appendChild(messageElement);
        scrollToBottom();
    }
    
    // Функция показа индикатора ожидания ответа
    function showTypingIndicator() {
        const indicatorElement = document.createElement('div');
        indicatorElement.className = 'message assistant typing-indicator';
        indicatorElement.innerHTML = `
            <div class="message-content">
                <div class="message-bubble">
                    <div class="loading-dots">
                        <span></span>
                        <span></span>
                        <span></span>
                    </div>
                </div>
            </div>
        `;
        
        chatMessages.appendChild(indicatorElement);
        scrollToBottom();
    }
    
    // Функция удаления индикатора ожидания
    function removeTypingIndicator() {
        const indicator = document.querySelector('.typing-indicator');
        if (indicator) {
            chatMessages.removeChild(indicator);
        }
    }
    
    // Функция прокрутки чата вниз
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Загрузка истории чата при открытии страницы
    async function loadChatHistory() {
        try {
            const response = await fetch('/api/history');
            if (response.ok) {
                const history = await response.json();
                
                if (history.length > 0) {
                    // Очищаем контейнер сообщений (удаляем приветственное сообщение)
                    chatMessages.innerHTML = '';
                    
                    // Добавляем все сообщения из истории
                    history.forEach(msg => {
                        addMessage(msg.content, msg.role === 'user' ? 'user' : 'assistant');
                    });
                }
            }
        } catch (error) {
            console.error('Ошибка при загрузке истории чата:', error);
        }
    }
    
    // Загружаем историю при инициализации
    loadChatHistory();
}); 