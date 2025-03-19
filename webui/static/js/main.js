document.addEventListener('DOMContentLoaded', () => {
    // Основные элементы интерфейса
    const chatForm = document.getElementById('chatForm');
    const userInput = document.getElementById('userInput');
    const chatMessages = document.getElementById('chatMessages');
    const sendButton = document.getElementById('sendButton');
    const clearChatButton = document.getElementById('clearChat');
    
    // Элементы для работы с сайдбаром
    const sidebar = document.getElementById('sidebar');
    const toggleSidebarBtn = document.getElementById('toggleSidebarBtn');
    const showSidebarBtn = document.getElementById('showSidebarBtn');
    const chatHistory = document.getElementById('chatHistory');
    const newChatBtn = document.getElementById('newChatBtn');
    
    // Для взаимодействия с анимацией сферы
    const sphereCanvas = document.getElementById('sphereCanvas');
    let animationEvent = new CustomEvent('animationUpdate', { detail: { type: 'idle' } });
    
    // Для работы с чатами
    let currentChatId = 'default';
    let chats = {
        'default': {
            id: 'default',
            title: 'Новый чат',
            messages: []
        }
    };
    
    // Загружаем сохраненные чаты из localStorage
    function loadChats() {
        const savedChats = localStorage.getItem('voxglow_chats');
        if (savedChats) {
            try {
                chats = JSON.parse(savedChats);
                
                // Если нет активного чата, используем первый доступный
                if (!chats[currentChatId]) {
                    currentChatId = Object.keys(chats)[0] || 'default';
                }
                
                // Очищаем историю чатов перед добавлением
                chatHistory.innerHTML = '';
                
                // Добавляем чаты в интерфейс
                Object.values(chats).forEach(chat => {
                    addChatToHistory(chat.id, chat.title);
                });
                
                // Активируем текущий чат
                const activeChatElement = chatHistory.querySelector(`[data-chat-id="${currentChatId}"]`);
                if (activeChatElement) {
                    activeChatElement.classList.add('active');
                    loadChatMessages(currentChatId);
                }
            } catch (error) {
                console.error('Ошибка при загрузке чатов из localStorage:', error);
                // Если произошла ошибка, используем пустой набор чатов
                chats = {
                    'default': {
                        id: 'default',
                        title: 'Новый чат',
                        messages: []
                    }
                };
            }
        }
    }
    
    // Сохраняем чаты в localStorage
    function saveChats() {
        try {
            localStorage.setItem('voxglow_chats', JSON.stringify(chats));
        } catch (error) {
            console.error('Ошибка при сохранении чатов в localStorage:', error);
        }
    }
    
    // Добавляем чат в историю
    function addChatToHistory(chatId, title) {
        const chatElement = document.createElement('div');
        chatElement.className = 'chat-history-item';
        chatElement.dataset.chatId = chatId;
        chatElement.innerHTML = `
            <span>${title}</span>
            <button class="delete-chat-btn" data-chat-id="${chatId}">
                <svg xmlns="http://www.w3.org/2000/svg" width="12" height="12" fill="currentColor" viewBox="0 0 16 16">
                    <path d="M4.646 4.646a.5.5 0 0 1 .708 0L8 7.293l2.646-2.647a.5.5 0 0 1 .708.708L8.707 8l2.647 2.646a.5.5 0 0 1-.708.708L8 8.707l-2.646 2.647a.5.5 0 0 1-.708-.708L7.293 8 4.646 5.354a.5.5 0 0 1 0-.708z"/>
                </svg>
            </button>
        `;
        
        // Добавляем обработчик для выбора чата
        chatElement.addEventListener('click', (e) => {
            // Игнорируем клик на кнопке удаления
            if (e.target.closest('.delete-chat-btn')) return;
            
            // Убираем класс active у всех чатов
            document.querySelectorAll('.chat-history-item').forEach(item => {
                item.classList.remove('active');
            });
            
            // Добавляем класс active текущему чату
            chatElement.classList.add('active');
            
            // Загружаем сообщения для выбранного чата
            currentChatId = chatId;
            loadChatMessages(chatId);
            
            // На мобильных устройствах скрываем сайдбар после выбора чата
            if (window.innerWidth <= 1024) {
                sidebar.classList.remove('visible');
            }
        });
        
        // Добавляем обработчик для удаления чата
        const deleteBtn = chatElement.querySelector('.delete-chat-btn');
        deleteBtn.addEventListener('click', () => {
            deleteChat(chatId);
        });
        
        chatHistory.appendChild(chatElement);
    }
    
    // Удаление чата
    function deleteChat(chatId) {
        if (Object.keys(chats).length <= 1) {
            // Не удаляем последний чат
            alert('Нельзя удалить последний чат');
            return;
        }
        
        // Удаляем чат из списка
        delete chats[chatId];
        saveChats();
        
        // Удаляем элемент из DOM
        const chatElement = chatHistory.querySelector(`[data-chat-id="${chatId}"]`);
        if (chatElement) {
            chatElement.remove();
        }
        
        // Если удаляем текущий чат, переключаемся на другой
        if (chatId === currentChatId) {
            currentChatId = Object.keys(chats)[0];
            const newActiveChat = chatHistory.querySelector(`[data-chat-id="${currentChatId}"]`);
            if (newActiveChat) {
                newActiveChat.classList.add('active');
            }
            loadChatMessages(currentChatId);
        }
    }
    
    // Создание нового чата
    function createNewChat() {
        const chatId = 'chat_' + Date.now();
        const title = 'Новый чат';
        
        // Добавляем чат в список
        chats[chatId] = {
            id: chatId,
            title: title,
            messages: []
        };
        
        saveChats();
        
        // Добавляем чат в DOM
        addChatToHistory(chatId, title);
        
        // Активируем новый чат
        document.querySelectorAll('.chat-history-item').forEach(item => {
            item.classList.remove('active');
        });
        
        const newChatElement = chatHistory.querySelector(`[data-chat-id="${chatId}"]`);
        if (newChatElement) {
            newChatElement.classList.add('active');
        }
        
        currentChatId = chatId;
        loadChatMessages(chatId);
    }
    
    // Загрузка сообщений для выбранного чата
    function loadChatMessages(chatId) {
        chatMessages.innerHTML = '';
        
        if (chats[chatId] && chats[chatId].messages && chats[chatId].messages.length > 0) {
            // Добавляем сообщения из истории
            chats[chatId].messages.forEach(msg => {
                addMessage(msg.content, msg.role, msg.isError, false);
            });
        } else {
            // Если нет сообщений, добавляем приветственное сообщение
            chatMessages.innerHTML = `
                <div class="message assistant visible">
                    <div class="message-content">
                        <div class="message-bubble">
                            <p>Привет! Я Кэролайн, ваш ассистент. Чем я могу помочь вам сегодня?</p>
                        </div>
                    </div>
                </div>
            `;
        }
    }
    
    // Управление видимостью сайдбара
    toggleSidebarBtn.addEventListener('click', () => {
        sidebar.classList.add('collapsed');
        showSidebarBtn.classList.add('visible');
    });
    
    showSidebarBtn.addEventListener('click', () => {
        sidebar.classList.remove('collapsed');
        sidebar.classList.add('visible');
        showSidebarBtn.classList.remove('visible');
    });
    
    // Обработчик для создания нового чата
    newChatBtn.addEventListener('click', createNewChat);
    
    // Автоматическое изменение высоты текстового поля
    userInput.addEventListener('input', () => {
        // Сброс высоты перед расчетом
        userInput.style.height = 'auto';
        // Установка высоты на основе содержимого
        userInput.style.height = (userInput.scrollHeight) + 'px';
        
        // Активация/деактивация кнопки отправки
        sendButton.disabled = userInput.value.trim() === '';
        
        // Отправляем событие для анимации - печатание
        if (userInput.value.trim() !== '') {
            animationEvent = new CustomEvent('animationUpdate', { detail: { type: 'typing' } });
            sphereCanvas.dispatchEvent(animationEvent);
        }
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
        
        // Анимация - сообщение отправлено
        animationEvent = new CustomEvent('animationUpdate', { detail: { type: 'message-sent' } });
        sphereCanvas.dispatchEvent(animationEvent);
        
        // Добавление сообщения пользователя в чат
        addMessage(message, 'user');
        
        // Обновляем заголовок чата, если это первое сообщение
        if (!chats[currentChatId].messages || chats[currentChatId].messages.length === 0) {
            // Используем первые 20 символов сообщения как заголовок чата
            const newTitle = message.length > 20 ? message.substring(0, 20) + '...' : message;
            chats[currentChatId].title = newTitle;
            
            // Обновляем заголовок в DOM
            const chatElement = chatHistory.querySelector(`[data-chat-id="${currentChatId}"]`);
            if (chatElement) {
                const titleSpan = chatElement.querySelector('span');
                if (titleSpan) {
                    titleSpan.textContent = newTitle;
                }
            }
            
            saveChats();
        }
        
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
                // Анимация - получен ответ
                animationEvent = new CustomEvent('animationUpdate', { detail: { type: 'message-received' } });
                sphereCanvas.dispatchEvent(animationEvent);
                
                // Добавление ответа ассистента
                addMessage(data.message, 'assistant');
            } else {
                // Обработка ошибки
                console.error('Ошибка при получении ответа:', data.error || 'Неизвестная ошибка');
                addMessage('Извините, произошла ошибка при обработке вашего запроса. Пожалуйста, попробуйте еще раз.', 'assistant', true);
                
                // Анимация - ошибка
                animationEvent = new CustomEvent('animationUpdate', { detail: { type: 'error' } });
                sphereCanvas.dispatchEvent(animationEvent);
            }
        } catch (error) {
            // Удаляем индикатор загрузки
            removeTypingIndicator();
            console.error('Ошибка при отправке запроса:', error);
            addMessage('Извините, не удалось подключиться к серверу. Пожалуйста, проверьте соединение и попробуйте снова.', 'assistant', true);
            
            // Анимация - ошибка
            animationEvent = new CustomEvent('animationUpdate', { detail: { type: 'error' } });
            sphereCanvas.dispatchEvent(animationEvent);
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
                // Очистка текущего чата
                chats[currentChatId].messages = [];
                saveChats();
                
                // Очистка UI чата (кроме приветственного сообщения)
                chatMessages.innerHTML = `
                    <div class="message assistant visible">
                        <div class="message-content">
                            <div class="message-bubble">
                                <p>Привет! Я Кэролайн, ваш ассистент. Чем я могу помочь вам сегодня?</p>
                            </div>
                        </div>
                    </div>
                `;
                
                // Анимация - сброс состояния
                animationEvent = new CustomEvent('animationUpdate', { detail: { type: 'reset' } });
                sphereCanvas.dispatchEvent(animationEvent);
            }
        } catch (error) {
            console.error('Ошибка при очистке истории:', error);
        }
    });
    
    // Функция добавления сообщения в чат
    function addMessage(content, sender, isError = false, saveToHistory = true) {
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
        
        // Добавляем эффект появления
        setTimeout(() => {
            messageElement.classList.add('visible');
        }, 10);
        
        // Сохраняем сообщение в историю чата
        if (saveToHistory) {
            if (!chats[currentChatId].messages) {
                chats[currentChatId].messages = [];
            }
            
            chats[currentChatId].messages.push({
                role: sender,
                content: content,
                isError: isError,
                timestamp: Date.now()
            });
            
            saveChats();
        }
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
        
        // Добавляем эффект появления
        setTimeout(() => {
            indicatorElement.classList.add('visible');
        }, 10);
    }
    
    // Функция удаления индикатора ожидания
    function removeTypingIndicator() {
        const indicator = document.querySelector('.typing-indicator');
        if (indicator) {
            // Добавляем эффект исчезновения
            indicator.classList.add('fade-out');
            
            // Удаляем элемент после завершения анимации
            setTimeout(() => {
                if (indicator.parentNode) {
                    chatMessages.removeChild(indicator);
                }
            }, 300);
        }
    }
    
    // Функция прокрутки чата вниз
    function scrollToBottom() {
        chatMessages.scrollTop = chatMessages.scrollHeight;
    }
    
    // Адаптация интерфейса при изменении размера окна
    window.addEventListener('resize', () => {
        if (window.innerWidth > 1024) {
            sidebar.classList.remove('visible');
            sidebar.classList.remove('collapsed');
            showSidebarBtn.classList.remove('visible');
        } else {
            sidebar.classList.add('collapsed');
            showSidebarBtn.classList.add('visible');
        }
    });
    
    // Инициализация при загрузке страницы
    function init() {
        // Загружаем сохраненные чаты
        loadChats();
        
        // Инициализируем состояние сайдбара в зависимости от ширины экрана
        if (window.innerWidth <= 1024) {
            sidebar.classList.add('collapsed');
            showSidebarBtn.classList.add('visible');
        }
        
        // Эффект появления для чата
        setTimeout(() => {
            document.body.classList.add('loaded');
        }, 500);
    }
    
    // Запускаем инициализацию
    init();
}); 