from flask import Flask, render_template, request, jsonify
import sys
import os
import json

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

# История разговора
conversation_history = []

@app.route('/')
def index():
    """Отображает главную страницу веб-интерфейса"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Обрабатывает запросы чата и возвращает ответы от ассистента"""
    data = request.json
    user_message = data.get('message', '')
    
    if not user_message:
        return jsonify({'error': 'Пустое сообщение'}), 400
    
    # Сохраняем сообщение пользователя в истории
    conversation_history.append({'role': 'user', 'content': user_message})
    
    # Получаем ответ от ассистента
    try:
        response = Ollama_Function_Main(user_message)
        
        # Сохраняем ответ ассистента в истории
        conversation_history.append({'role': 'assistant', 'content': response})
        
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

@app.route('/api/history', methods=['GET'])
def get_history():
    """Возвращает историю разговора"""
    return jsonify(conversation_history)

@app.route('/api/clear_history', methods=['POST'])
def clear_history():
    """Очищает историю разговора"""
    global conversation_history
    conversation_history = []
    return jsonify({'success': True})

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000) 