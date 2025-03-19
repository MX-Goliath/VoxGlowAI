#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Скрипт запуска веб-интерфейса для VoxGlowAI.
"""

import os
import sys

# Добавляем текущую директорию в путь импорта
current_dir = os.path.dirname(os.path.abspath(__file__))
sys.path.append(current_dir)

# Импортируем приложение Flask из текущей директории
from app import app

if __name__ == '__main__':
    print("Запуск веб-интерфейса VoxGlowAI...")
    print("Веб-интерфейс доступен по адресу: http://localhost:5000")
    app.run(debug=True, host='0.0.0.0', port=5000) 