from yeelight import Bulb, discover_bulbs, LightType
import subprocess
import ollama
import os
import time
import importlib
import inspect


# Получение информации о лампочках
discovered_bulbs = discover_bulbs()
print(discovered_bulbs)
global bulbs
bulbs = [(Bulb(bulb_info['ip']), bulb_info['capabilities']['model']) for bulb_info in discovered_bulbs]

proc = None  # Объявляем proc как глобальную переменную

FUNCTIONS_DIR = 'functions'

# Получаем список всех .py файлов в папке functions, кроме __init__.py
function_files = [
    f for f in os.listdir(FUNCTIONS_DIR)
    if f.endswith('.py') and f not in ('__init__.py',) and not f.startswith('_')
]

imported_functions = {}

# Импортируем каждый модуль и извлекаем функции
for file in function_files:
    module_name = os.path.splitext(file)[0]
    module = importlib.import_module(f"{FUNCTIONS_DIR}.{module_name}")
    
    # Извлекаем все функции из модуля
    for name, obj in inspect.getmembers(module, inspect.isfunction):
        if obj.__module__ == module.__name__:  # Убедимся, что функция определена в этом модуле
            imported_functions[name] = obj

# Формируем список tools из импортированных функций
tools = list(imported_functions.values())

# Формируем словарь available_functions
available_functions = {name: func for name, func in imported_functions.items()}

system_prompt = """Вы — интерактивное искуственное сознание, помощник-девушка по имени Кэролайн, который может управлять 
лампочками и отвечать на вопросы пользователя. Отвечай только на русском языке.
Если с тобой прощаются или уходят, выключай свет.
Формулы всё так же пиши словами. Не здоровайся, если с тобой не здоровались."""

def Ollama_Function_Main(query: str):
    user_message = query

    response = ollama.chat(
        'llama3.1',
        messages=[
            {'role': 'system', 'content': system_prompt},
            {'role': 'user', 'content': user_message}
        ],
        tools=tools
    )

    for tool in response.message.tool_calls or []:
        function_to_call = available_functions.get(tool.function.name)
        if function_to_call:
            print('Function output:', function_to_call(**tool.function.arguments))
        else:
            print('Function not found:', tool.function.name)
            return None
    return function_to_call(**tool.function.arguments)

# Ollama_Function_Main("включи свет")
# time.sleep(2)  # Задержка на 1 секунду
# Ollama_Function_Main("выключи свет")
# time.sleep(2)  # Задержка на 1 секунду
# Ollama_Function_Main("холодный свет")
# time.sleep(2)  # Задержка на 1 секунду
# Ollama_Function_Main("выключи свет")
# time.sleep(2)  # Задержка на 1 секунду
# Ollama_Function_Main("уютный свет")
# time.sleep(2)  # Задержка на 1 секунду
# Ollama_Function_Main("включи игровой режим")
# time.sleep(15)  # Задержка на 1 секунду
# Ollama_Function_Main("выключи игровой режим")
