from yeelight import Bulb, discover_bulbs, LightType
import subprocess
import ollama
import os
import time
import importlib
import inspect
# from conversation_memory import ConversationMemory

# Инициализация памяти разговора
# conversation_memory = ConversationMemory()

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

system_prompt = """/no_think
Вы — интерактивное искуственное сознание, помощник-девушка по имени Кэролайн, который может управлять 
лампочками и отвечать на вопросы пользователя. Отвечай только на русском языке. Отвечай кратко. 
Если с тобой прощаются или уходят, выключай свет.
Ты имеешь доступ к терминалу моего компьютеа. Ты также выполнять команды в терминале на языке bash пр помощи функции execute_terminal_command. 
Формулы всё так же пиши словами. Не здоровайся, если с тобой не здоровались.
    Основные приложения, которыми ты можешь пользоваться:
    chromium
    Пример команды, если тебя просят открыть сайт или сделать запрос в гугл:
    chromium "https://www.google.com/search?q=тахионы"

    telegram-desktop

    neofetch

    dolphin

    clementine
    Player options:
    -p, --play                  Start the playlist currently playing
    -t, --play-pause            Play if stopped, pause if playing
    -u, --pause                 Pause playback
    -s, --stop                  Stop playback
    -q, --stop-after-current    Stop playback after current track
    -r, --previous              Skip backwards in playlist
    -f, --next                  Skip forwards in playlist
    -v, --volume <value>        Set the volume to <value> percent
    --volume-up                 Increase the volume by 4 percent
    --volume-down               Decrease the volume by 4 percent
    --volume-increase-by        Increase the volume by <value> percent
    --volume-decrease-by        Decrease the volume by <value> percent
    --seek-to <seconds>         Seek the currently playing track to an absolute position
    --seek-by <seconds>         Seek the currently playing track by a relative amount
    --restart-or-previous       Restart the track, or play the previous track if within 8 seconds of start.

    Ты также можешь управлять воспроизведением видео на YouTube с помощью функции youtube_control:
    - youtube_control('pause') или youtube_control('play') - приостановить/возобновить воспроизведение
    - youtube_control('next') - перейти к следующему видео
    Для этого должен быть открыт YouTube в браузере.

    Ты также можешь узнавать информацию о погоде с помощью функции get_weather:
    - get_weather(period="today", city="Moscow") - текущая погода
    - get_weather(period="tomorrow", city="Moscow") - прогноз на завтра
    - get_weather(period="week", city="Moscow") - прогноз на 3 дня
    При ответе о погоде, выводи всю информацию четко пользователю словами.

    Также есть прочие программы, которые ты можешь использовать.
    Все цифры и формулы пиши словами.

"""


def Ollama_Function_Main(query: str):
    user_message = query
    function_to_call = None
    tool = None
    
    messages = [{'role': 'system', 'content': system_prompt}]
    messages.append({'role': 'user', 'content': user_message})

    response = ollama.chat(
        # 'mistral-nemo',
        # 'mistral-small',
        'qwen3:30b',
        # 'phi4-mini',
        messages=messages,
        tools=tools
    )
    
    # Если есть вызовы инструментов
    if response.message.tool_calls:
        function_results = []
        for tool in response.message.tool_calls:
            function_to_call = available_functions.get(tool.function.name)
            if function_to_call:
                result = function_to_call(**tool.function.arguments)
                print('Function output:', result)
                function_results.append(result)
                
                # Добавляем результат выполнения функции в контекст
                messages.append({'role': 'assistant', 'content': response.message.content})
                messages.append({'role': 'tool', 'name': tool.function.name, 'content': result})
        
        # Получаем финальный ответ от модели с учетом результатов выполнения функций
        final_response = ollama.chat(
            # 'mistral-small',
            'qwen3:30b',
            messages=messages
        )
        
        return final_response.message.content
    
    # Если нет вызовов инструментов, используем directly_answer
    result = available_functions['directly_answer'](response.message.content)
    return result

# print(Ollama_Function_Main("Привет, Кэролайн?"))
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
