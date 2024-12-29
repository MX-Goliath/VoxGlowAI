from yeelight import Bulb, discover_bulbs, LightType
import subprocess
import os


discovered_bulbs = discover_bulbs()
bulbs = [(Bulb(bulb_info['ip']), bulb_info['capabilities']['model']) for bulb_info in discovered_bulbs]

def turn_all_on():
    """
    Включение всех лампочек
    """
    global bulbs  # Указываем, что используется глобальная переменная
    print("Включаем все лампы")
    for bulb, model in bulbs:
        bulb.turn_on()
    return "Свет включен"

def set_brightness(level: int):
    """
    Установить яркость лампочек

    Аргументы:
        level: Уровень яркости в процентах, целое число

    Возвращает:
        str: Сообщение о результате установки яркости
    """
    level = int(level)  # Преобразуем level в целое число

    print(f"Устанавливаем яркость на {level}%")
    for bulb, model in bulbs:
        bulb.set_brightness(level)
    return f"Яркость установлена  {level}%."

def night_light():
    """
    Установить лампочки в режим ночного освещения

    Возвращает:
        str: Сообщение о результате установки игрового режима освещения
    """
    turn_all_on()
    for bulb, model in bulbs:
        bulb.set_color_temp(3500)
        if model == 'lamp15':
            bulb.set_color_temp(3500, light_type=LightType.Ambient)
            bulb.set_brightness(30, light_type=LightType.Ambient)
        bulb.set_brightness(30)
    return "Лампочки установлены в режим ночного освещения."


def standard():
    """
    Установить лампочки в режим стандратного освещения

    Возвращает:
        str: Сообщение о результате установки игрового режима освещения
    """
    turn_all_on()
    for bulb, model in bulbs:
        bulb.set_color_temp(4000)
        if model == 'lamp15':
            bulb.set_color_temp(4000, light_type=LightType.Ambient)
            bulb.set_brightness(100, light_type=LightType.Ambient)
        bulb.set_brightness(100)
    return "Лампочки установлены в стандартный режим."

def turn_all_off():
    """
    Выключение всех лампочек
    """
    print("Выключаем все лампы")
    for bulb, model in bulbs:
        bulb.turn_off()
    return "Свет выключен"

def cozy_home():
    """
    Установить лампочки в игровой режим уютного дома

    Возвращает:
        str: Сообщение о результате установки игрового режима освещения
    """
    turn_all_on()
    for bulb, model in bulbs:
        bulb.set_color_temp(3500)
        if model == 'lamp15':
            bulb.set_color_temp(3500, light_type=LightType.Ambient)
            bulb.set_brightness(80, light_type=LightType.Ambient)
        bulb.set_brightness(80)
    return "Лампочки установлены в уютный домашний режим."

def cold_light():
    """
    Установить лампочки в режим холодного освещения

    Возвращает:
        str: Сообщение о результате установки игрового режима освещения
    """
    turn_all_on()
    for bulb, model in bulbs:
        bulb.set_color_temp(5000)
        if model == 'lamp15':
            bulb.set_color_temp(5000, light_type=LightType.Ambient)
            bulb.set_brightness(100, light_type=LightType.Ambient)
        bulb.set_brightness(100)
    return "Лампочки установлены в холодный свет."

def game_mode_on():
    """
    Установить лампочки в игровой режим освещения и открыть стим

    Возвращает:
        str: Сообщение о результате установки игрового режима освещения и открытия стим
    """
    turn_all_on()
    for bulb, model in bulbs:
        bulb.set_color_temp(3500)
        if model == 'lamp15':
            bulb.set_rgb(105, 144, 199, light_type=LightType.Ambient)
            bulb.set_brightness(100, light_type=LightType.Ambient)
            bulb.turn_off()
        else:
            bulb.turn_off()
            bulb.set_brightness(0)
        global proc
    # os.system("nmcli connection down 'Проводное подключение 1'")
    # Запуск Steam в режиме Big Picture в отдельном процессе
    proc = subprocess.Popen(["steam", "-udpforce", "-tenfoot"])
    return "Включаю игровой режим."

def game_mode_off():
    global proc
    if proc and proc.poll() is None:  # Проверяем, что proc не None и процесс еще не завершился
        proc.kill()  # Лучше использовать terminate(), а затем kill(), если необходимо
        proc.wait()  # Даем процессу время на корректное завершение
    os.system("killall steam")
    standard()