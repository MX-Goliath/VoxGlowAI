import requests
import datetime

def get_weather(period: str = "today", city: str = "Moscow") -> str:
    """
    Получает информацию о погоде через сервис wttr.in
    
    Args:
        period: Период прогноза ("today", "tomorrow", "week")
        city: Название города (по умолчанию "Moscow")
        
    Returns:
        str: Отформатированная информация о погоде
    """
    try:
        # Формируем URL с параметрами
        # ?format=j1 - получаем данные в формате JSON
        # ?lang=ru - получаем данные на русском языке
        # ?m - метрическая система (градусы Цельсия)
        url = f"https://wttr.in/{city}?format=j1&lang=ru&m"
        
        response = requests.get(url, headers={'Accept-Language': 'ru'})
        data = response.json()
        
        if period.lower() == "today":
            current = data['current_condition'][0]
            temp = current['temp_C']
            feels_like = current['FeelsLikeC']
            description = current['lang_ru'][0]['value']
            humidity = current['humidity']
            wind = current['windspeedKmph']
            
            return (f"Текущая погода в городе {city}:\n"
                    f"Температура: {temp}°C, ощущается как {feels_like}°C\n"
                    f"Погодные условия: {description}\n"
                    f"Влажность: {humidity}%\n"
                    f"Скорость ветра: {round(float(wind) * 0.28)} м/с")  # Конвертируем км/ч в м/с
                    
        elif period.lower() == "tomorrow":
            tomorrow = data['weather'][1]  # Индекс 1 - завтрашний день
            temp_max = tomorrow['maxtempC']
            temp_min = tomorrow['mintempC']
            description = tomorrow['hourly'][4]['lang_ru'][0]['value']  # Берем погоду на полдень
            humidity = tomorrow['hourly'][4]['humidity']
            wind = tomorrow['hourly'][4]['windspeedKmph']
            
            return (f"Прогноз погоды на завтра в городе {city}:\n"
                    f"Температура: от {temp_min}°C до {temp_max}°C\n"
                    f"Погодные условия: {description}\n"
                    f"Влажность: {humidity}%\n"
                    f"Скорость ветра: {round(float(wind) * 0.28)} м/с")
                    
        elif period.lower() == "week":
            result = f"Прогноз погоды на ближайшие дни в городе {city}:\n"
            
            for i, day in enumerate(data['weather']):
                if i >= 3:  # wttr.in дает прогноз на 3 дня
                    break
                    
                date = datetime.datetime.strptime(day['date'], '%Y-%m-%d')
                day_name = date.strftime('%A')
                
                # Перевод дней недели
                day_translations = {
                    'Monday': 'Понедельник',
                    'Tuesday': 'Вторник',
                    'Wednesday': 'Среда',
                    'Thursday': 'Четверг',
                    'Friday': 'Пятница',
                    'Saturday': 'Суббота',
                    'Sunday': 'Воскресенье'
                }
                day_name = day_translations.get(day_name, day_name)
                
                temp_max = day['maxtempC']
                temp_min = day['mintempC']
                description = day['hourly'][4]['lang_ru'][0]['value']  # Погода в полдень
                
                result += f"\n{day_name} ({day['date']}): {temp_min}°C до {temp_max}°C, {description}"
            
            return result
            
        else:
            return "Неверно указан период. Используйте 'today', 'tomorrow' или 'week'."
            
    except requests.exceptions.RequestException as e:
        return f"Ошибка при соединении с сервером погоды: {str(e)}"
    except Exception as e:
        return f"Произошла ошибка при получении данных о погоде: {str(e)}" 