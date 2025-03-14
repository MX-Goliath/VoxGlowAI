import subprocess
import os
import shlex

def execute_terminal_command(command: str) -> str:
    """
    Выполняет команду в терминале и возвращает результат.


    
    Args:
        command: Строка с командой для выполнения в терминале
        
    Returns:
        str: Результат выполнения команды или сообщение об ошибке
    """
    try:
        # Используем shlex для безопасного разделения аргументов команды
        args = shlex.split(command)
        
        # Проверка на потенциально опасные команды
        dangerous_commands = ['rm -rf', 'mkfs', 'dd', ':(){', 'sudo rm', '> /dev/sda']
        if any(dangerous in command for dangerous in dangerous_commands):
            return "Отказано в выполнении: потенциально опасная команда."
        
        # Выполняем команду и получаем вывод
        process = subprocess.Popen(
            args,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
            text=True,
            shell=False  # Безопаснее использовать shell=False
        )
        
        # Получаем вывод команды
        stdout, stderr = process.communicate(timeout=30)  # Таймаут 30 секунд
        
        # Формируем результат
        if process.returncode == 0:
            result = stdout.strip()
            if not result:
                result = "Команда выполнена успешно (без вывода)."
            return result
        else:
            return f"Ошибка выполнения команды: {stderr.strip()}"
            
    except subprocess.TimeoutExpired:
        return "Превышено время ожидания выполнения команды."
    except Exception as e:
        return f"Произошла ошибка: {str(e)}" 