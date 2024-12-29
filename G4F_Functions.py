import re
import os
import importlib
import inspect
from yeelight import Bulb, discover_bulbs, LightType
from g4f import ChatCompletion

# ------------------------------- #
#         ОБЩИЕ НАСТРОЙКИ        #
# ------------------------------- #

# Системный промпт с явными инструкциями и примерами вызовов функций
system_prompt = """Вы — интерактивное искусственное сознание, помощник-девушка по имени Кэролайн, который может управлять 
лампочками и отвечать на вопросы пользователя. Отвечай только на русском языке.
Если с тобой прощаются или уходят, выключай свет.
Формулы всё так же пиши словами. Не здоровайся, если с тобой не здоровались.
Если нужно вызвать функцию, используй следующий формат: #function_name(arg1=value1, arg2=value2).
Примеры:
turn_all_on() # Включить все лампы
turn_all_off() # Выключить все лампы
set_brightness(level=50) # установить заданный уровень яркости
get_weather() # получить данные о погоде
night_light()  # включить ночной свет
cozy_home() # включить уютный домашний свет
cold_light() # включить холодный свет
game_mode_on() # включить игровой режим
game_mode_off() # выключить игровой режим
"""

# Получение информации о лампочках
discovered_bulbs = discover_bulbs()
print("Обнаруженные лампочки:", discovered_bulbs)
bulbs = [(Bulb(bulb_info['ip']), bulb_info['capabilities']['model']) for bulb_info in discovered_bulbs]


FUNCTIONS_DIR = 'functions'

# Убедитесь, что папка 'functions' существует
if not os.path.isdir(FUNCTIONS_DIR):
    print(f"Папка '{FUNCTIONS_DIR}' не найдена. Создайте её и добавьте функции.")
    exit(1)

function_files = [
    f for f in os.listdir(FUNCTIONS_DIR)
    if f.endswith('.py') and f not in ('__init__.py',) and not f.startswith('_')
]

imported_functions = {}

# Импортируем модули и извлекаем функции
for file in function_files:
    module_name = os.path.splitext(file)[0]
    try:
        module = importlib.import_module(f"{FUNCTIONS_DIR}.{module_name}")
    except Exception as e:
        print(f"Ошибка при импорте модуля {module_name}: {e}")
        continue

    for name, obj in inspect.getmembers(module, inspect.isfunction):
        if obj.__module__ == module.__name__:
            imported_functions[name] = obj

# Доступные функции
available_functions = {name: func for name, func in imported_functions.items()}


def G4F_Function_Main(query: str):
    user_message = query

    messages = [
        {'role': 'system', 'content': system_prompt},
        {'role': 'user', 'content': user_message}
    ]

    try:
        response = ChatCompletion.create(
            model="gpt-4o-mini",
            messages=messages,
            provider="DDG"
        )
    except Exception as e:
        return f"Ошибка при запросе к модели: {e}"

    print("Ответ модели:", response)  # Для отладки

    # Проверка на вызов функции с использованием регулярного выражения
    # Учтём, что внутри скобок могут быть пробелы, и аргументы могут быть без значения
    function_call_pattern = r"#(\w+)\s*\(\s*(.*?)\s*\)"
    match = re.search(function_call_pattern, response)

    if match:
        function_name = match.group(1)
        function_args_str = match.group(2)
        function_args = {}

        print(f"Найдена функция: {function_name} с аргументами: {function_args_str}")  # Для отладки

        # Разбираем аргументы (например, level=50)
        if function_args_str:
            # Разделяем аргументы по запятым, учитывая возможные пробелы
            args_list = [arg.strip() for arg in function_args_str.split(',') if arg.strip()]
            for arg in args_list:
                if '=' in arg:
                    key, value = arg.split('=', 1)
                    key = key.strip()
                    value = value.strip()
                    function_args[key] = value
                else:
                    # Если аргумент без ключа, добавляем его с именем 'arg'
                    function_args['arg'] = arg.strip()

        # Преобразуем аргументы в нужные типы
        if function_name in available_functions:
            func = available_functions[function_name]
            try:
                # Получаем сигнатуру функции для определения типов аргументов
                signature = inspect.signature(func)
                for param in signature.parameters.values():
                    if param.name in function_args:
                        expected_type = param.annotation
                        if expected_type == int:
                            try:
                                function_args[param.name] = int(function_args[param.name])
                            except ValueError:
                                print(f"Неверный тип для параметра {param.name}: ожидается integer.")
                                return f"Неверный тип для параметра {param.name}: ожидается integer."
                        elif expected_type == float:
                            try:
                                function_args[param.name] = float(function_args[param.name])
                            except ValueError:
                                print(f"Неверный тип для параметра {param.name}: ожидается float.")
                                return f"Неверный тип для параметра {param.name}: ожидается float."
                        elif expected_type == str:
                            function_args[param.name] = str(function_args[param.name])
                        # Добавьте другие типы при необходимости

                print(f"Вызов функции {function_name} с аргументами: {function_args}")  # Для отладки
                # Вызываем функцию
                result = func(**function_args)
                return result
            except Exception as e:
                return f"Ошибка при вызове функции {function_name}: {e}"
        else:
            return f"Функция {function_name} не найдена."
    else:
        # Если функция не вызвана, просто выводим ответ
        return response



response=G4F_Function_Main("Включи свет")
print("Ответ:", response)
