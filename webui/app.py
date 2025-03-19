from flask import Flask, render_template, request, jsonify
import sys
import os
import json
import uuid
import time

# Добавляем родительскую директорию в путь, чтобы импортировать модули
parent_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
sys.path.insert(0, parent_dir)

# Устанавливаем текущую директорию как родительскую для корректной работы с относительными путями
os.chdir(parent_dir)

# Импортируем функцию из основного проекта
from Ollama_Functions import Ollama_Function_Main

# Импортируем системный промпт из локального модуля
sys.path.append(os.path.dirname(os.path.abspath(__file__)))
from system_prompt import get_web_system_prompt

app = Flask(__name__)

# Загружаем системный промт для веб-интерфейса
SYSTEM_PROMPT = get_web_system_prompt()

# Хранилище чатов: { 'chat_id': { 'messages': [...], 'title': '...' } }
chats_storage = {}

@app.route('/')
def index():
    """Отображает главную страницу веб-интерфейса"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Обрабатывает запросы чата и возвращает ответы от ассистента"""
    data = request.json
    user_message = data.get('message', '')
    chat_id = data.get('chat_id', 'default')
    
    if not user_message:
        return jsonify({'error': 'Пустое сообщение'}), 400
    
    # Инициализируем чат, если его нет
    if chat_id not in chats_storage:
        chats_storage[chat_id] = {
            'messages': [],
            'title': 'Новый чат',
            'created_at': time.time()
        }
    
    # Сохраняем сообщение пользователя в истории
    chats_storage[chat_id]['messages'].append({
        'role': 'user', 
        'content': user_message,
        'timestamp': time.time()
    })
    
    # Получаем ответ от ассистента
    try:
        response = Ollama_Function_Main(user_message)
        
        # Сохраняем ответ ассистента в истории
        chats_storage[chat_id]['messages'].append({
            'role': 'assistant', 
            'content': response,
            'timestamp': time.time()
        })
        
        # Если это первое сообщение, обновляем заголовок чата
        if len(chats_storage[chat_id]['messages']) == 2:  # После получения первого ответа
            title = user_message[:30] + '...' if len(user_message) > 30 else user_message
            chats_storage[chat_id]['title'] = title
        
        return jsonify({
            'message': response,
            'success': True
        })
    except Exception as e:
        print(f"Ошибка при получении ответа: {e}")
        return jsonify({
            'error': 'Произошла ошибка при обработке запроса',
            'details': str(e),
            'success': False
        }), 500

@app.route('/api/chats', methods=['GET'])
def get_chats():
    """Возвращает список всех чатов"""
    # Преобразуем в список, сортируем по времени создания (новые сверху)
    chats_list = [
        {
            'id': chat_id,
            'title': chat_info['title'],
            'created_at': chat_info.get('created_at', 0),
            'message_count': len(chat_info['messages'])
        }
        for chat_id, chat_info in chats_storage.items()
    ]
    
    # Сортировка по времени создания (новые сверху)
    chats_list.sort(key=lambda x: x['created_at'], reverse=True)
    
    return jsonify(chats_list)

@app.route('/api/chats/<chat_id>', methods=['GET'])
def get_chat(chat_id):
    """Возвращает историю конкретного чата"""
    if chat_id not in chats_storage:
        return jsonify({'error': 'Чат не найден'}), 404
    
    return jsonify(chats_storage[chat_id])

@app.route('/api/chats/<chat_id>', methods=['DELETE'])
def delete_chat(chat_id):
    """Удаляет чат"""
    if chat_id in chats_storage:
        del chats_storage[chat_id]
    
    return jsonify({'success': True})

@app.route('/api/chats', methods=['POST'])
def create_chat():
    """Создает новый чат"""
    chat_id = f"chat_{uuid.uuid4().hex[:8]}"
    title = request.json.get('title', 'Новый чат')
    
    chats_storage[chat_id] = {
        'messages': [],
        'title': title,
        'created_at': time.time()
    }
    
    return jsonify({
        'id': chat_id,
        'title': title,
        'success': True
    })

@app.route('/api/chats/<chat_id>/clear', methods=['POST'])
def clear_chat(chat_id):
    """Очищает историю конкретного чата"""
    if chat_id not in chats_storage:
        return jsonify({'error': 'Чат не найден'}), 404
    
    chats_storage[chat_id]['messages'] = []
    
    return jsonify({'success': True})

@app.route('/api/clear_history', methods=['POST'])
def clear_history():
    """Очищает историю всех разговоров"""
    global chats_storage
    chats_storage = {}
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 