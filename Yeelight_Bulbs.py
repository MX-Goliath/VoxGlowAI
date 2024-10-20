from yeelight import Bulb, discover_bulbs, LightType

# Получение информации о лампочках
discovered_bulbs = discover_bulbs()
print(discovered_bulbs)

# Извлечение IP-адресов и создание объектов Bulb с сохранением модели лампы
bulbs = [(Bulb(bulb_info['ip']), bulb_info['capabilities']['model']) for bulb_info in discovered_bulbs]

# Функции управления лампами с проверкой модели
def turn_all_on():
    print("Включаем все лампы")
    for bulb, model in bulbs:
        bulb.turn_on()

def turn_all_off():
    print("Выключаем все лампы")
    for bulb, model in bulbs:
        bulb.turn_off()

def night_light():
    turn_all_on()
    for bulb, model in bulbs:
        bulb.set_color_temp(3500)
        if model == 'lamp15':
            bulb.set_color_temp(3500, light_type=LightType.Ambient)
            bulb.set_brightness(30, light_type=LightType.Ambient)
        bulb.set_brightness(30)

def cozy_home():
    turn_all_on()
    for bulb, model in bulbs:
        bulb.set_color_temp(3500)
        if model == 'lamp15':
            bulb.set_color_temp(3500, light_type=LightType.Ambient)
            bulb.set_brightness(80, light_type=LightType.Ambient)
        bulb.set_brightness(80)

def standard():
    turn_all_on()
    for bulb, model in bulbs:
        bulb.set_color_temp(4000)
        if model == 'lamp15':
            bulb.set_color_temp(4000, light_type=LightType.Ambient)
            bulb.set_brightness(100, light_type=LightType.Ambient)
        bulb.set_brightness(100)

def cold_light():
    turn_all_on()
    for bulb, model in bulbs:
        bulb.set_color_temp(5000)
        if model == 'lamp15':
            bulb.set_color_temp(5000, light_type=LightType.Ambient)
            bulb.set_brightness(100, light_type=LightType.Ambient)
        bulb.set_brightness(100)

def gamde_mode_light():
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
# Пример использования
standard()
# turn_all_on()
# Другие функции можно вызвать аналогичным образом
