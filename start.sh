#!/bin/bash

# Проверяем существование виртуальной среды
if [ ! -d "./.myenv" ]; then
    echo "Creating virtual environment..."
    python3 -m venv .myenv || { echo "Failed to create virtual environment"; exit 1; }
    
    # Исправлен путь к activate (добавлена точка)
    source ./.myenv/bin/activate
    
    echo "Installing dependencies from requirements.txt"
    pip install --upgrade pip
    if ! pip install -r requirements.txt; then
        echo "Failed to install packages. Trying alternative PyTorch sources..."
        
        # Удаляем проблемные строчки из requirements.txt временно
        sed -i '/torch @/d' requirements.txt
        sed -i '/torchaudio @/d' requirements.txt
        sed -i '/torchvision @/d' requirements.txt
        
        pip install -r requirements.txt || { echo "Final installation failed"; exit 1; }
        
        # Устанавливаем PyTorch через официальную команду для ROCm (стабильная версия)
        pip install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/nightly/rocm6.1
    fi
    
    deactivate
fi

# Активируем окружение
source ./.myenv/bin/activate

python ./Speech_Recognition.py || echo "Script exited with error $?"