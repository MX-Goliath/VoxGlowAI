import subprocess
import shlex
import time

def youtube_control(action: str) -> str:
    """
    Управляет воспроизведением видео в YouTube через симуляцию нажатий клавиш.
    
    Args:
        action: Действие для выполнения ('pause', 'play', 'next', 'prev', 'speed_up', 'speed_down')
        
    Returns:
        str: Результат выполнения команды или сообщение об ошибке
    """
    try:
        # Поиск окна Chromium с открытым YouTube
        # Сначала проверяем окно с YouTube в названии
        window_id = None
        
        # Проверяем окна с названием YouTube
        check_youtube = subprocess.run(
            ["xdotool", "search", "--onlyvisible", "--name", "YouTube"],
            capture_output=True,
            text=True
        )
        
        # Проверяем окна Chromium
        check_chromium = subprocess.run(
            ["xdotool", "search", "--onlyvisible", "--name", "Chromium"],
            capture_output=True,
            text=True
        )
        
        # Если нашли окно с YouTube, используем его ID
        if check_youtube.stdout.strip():
            window_ids = check_youtube.stdout.strip().split('\n')
            for wid in window_ids:
                if not wid:
                    continue
                    
                # Проверяем имя окна для подтверждения
                get_name = subprocess.run(
                    ["xdotool", "getwindowname", wid],
                    capture_output=True,
                    text=True
                )
                window_name = get_name.stdout.strip()
                
                # Если это действительно YouTube, используем это окно
                if "YouTube" in window_name:
                    window_id = wid
                    break
        
        # Если не нашли окно с YouTube напрямую, пробуем искать Chromium с YouTube в заголовке
        if not window_id and check_chromium.stdout.strip():
            window_ids = check_chromium.stdout.strip().split('\n')
            for wid in window_ids:
                if not wid:
                    continue
                    
                # Проверяем имя окна
                get_name = subprocess.run(
                    ["xdotool", "getwindowname", wid],
                    capture_output=True,
                    text=True
                )
                window_name = get_name.stdout.strip()
                
                # Если в заголовке есть YouTube, используем это окно
                if "YouTube" in window_name:
                    window_id = wid
                    break
        
        # Если не нашли окно с YouTube
        if not window_id:
            return "Не найдено открытое окно YouTube в Chromium. Пожалуйста, сначала откройте YouTube в браузере."
        
        # Фокусируемся на найденном окне
        subprocess.run(["xdotool", "windowactivate", window_id])
        # Добавляем паузу для надежного переключения фокуса
        time.sleep(0.5)
        
        # Выполняем действие
        if action.lower() == 'pause' or action.lower() == 'play':
            # Пробел для паузы/воспроизведения
            subprocess.run(["xdotool", "key", "space"])
            return "Воспроизведение поставлено на паузу/возобновлено."
            
        elif action.lower() == 'next':
            # Shift+N для следующего видео
            subprocess.run(["xdotool", "key", "shift+n"])
            return "Переход к следующему видео."
            
        elif action.lower() == 'prev':
            # Shift+P для предыдущего видео
            subprocess.run(["xdotool", "key", "shift+p"])
            return "Переход к предыдущему видео."
            
        elif action.lower() == 'speed_up':
            # Для YouTube в браузере просто точка
            subprocess.run(["xdotool", "key", "period"])
            return "Скорость воспроизведения увеличена."
            
        elif action.lower() == 'speed_down':
            # Для YouTube в браузере просто запятая
            subprocess.run(["xdotool", "key", "comma"])
            return "Скорость воспроизведения уменьшена."
            
        else:
            return f"Неизвестное действие: {action}. Доступные действия: pause/play, next, prev, speed_up, speed_down."
            
    except FileNotFoundError:
        return "Для управления YouTube требуется установить xdotool. Установите его командой 'sudo apt-get install xdotool'."
    except Exception as e:
        return f"Произошла ошибка при управлении YouTube: {str(e)}" 