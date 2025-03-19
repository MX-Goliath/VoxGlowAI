#!/bin/bash

# Скрипт запуска веб-интерфейса VoxGlowAI

# Определяем путь к директориям
SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
PROJECT_ROOT="$(cd "$SCRIPT_DIR/.." && pwd)"

# Активируем виртуальное окружение, или создаем его, если оно не существует
if [ -d "$PROJECT_ROOT/.myenv" ]; then
    echo "Активация виртуального окружения..."
    source "$PROJECT_ROOT/.myenv/bin/activate"
else
    echo "Виртуальное окружение не найдено. Создаем новое..."
    cd "$PROJECT_ROOT"
    python -m venv .myenv
    source "$PROJECT_ROOT/.myenv/bin/activate"
fi

# Проверяем, установлен ли Flask в виртуальном окружении
if ! python -c "import flask" &>/dev/null; then
    echo "Flask не установлен. Устанавливаем..."
    pip install flask
fi

# Запускаем веб-интерфейс из его директории
cd "$SCRIPT_DIR"
echo "Запуск веб-интерфейса VoxGlowAI..."
echo "Веб-интерфейс будет доступен по адресу: http://localhost:5000"

# Запуск приложения напрямую через Python
python -c "
from app import app
app.run(host='0.0.0.0', port=5000, debug=False)
"

# Деактивируем виртуальное окружение при выходе
deactivate 