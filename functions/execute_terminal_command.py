import subprocess
import os
import shlex

def execute_terminal_command(command: str) -> str:
    """
    Выполняет команду в терминале и возвращает результат.
    Команды, предназначенные для запуска в фоновом режиме (например, GUI-приложения),
    запускаются без ожидания их завершения.

    Args:
        command: Строка с командой для выполнения в терминале

    Returns:
        str: Результат выполнения команды, сообщение об ошибке,
             или сообщение о запуске команды в фоновом режиме.
    """
    try:
        # Используем shlex для безопасного разделения аргументов команды
        args = shlex.split(command)

        if not args:
            return "Ошибка: пустая команда."

        # Проверка на потенциально опасные команды
        dangerous_commands = ['rm -rf', 'mkfs', 'dd', ':(){', 'sudo rm', '> /dev/sda']
        if any(dangerous in command for dangerous in dangerous_commands):
            return "Отказано в выполнении: потенциально опасная команда."

        command_name = args[0]
        # Список команд, которые должны запускаться в фоновом режиме
        background_commands = ['dolphin', 'chromium', 'telegram-desktop', 'clementine']

        if command_name in background_commands:
            # Запускаем команду в фоновом режиме и не ждем ее завершения
            subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, shell=False)
            return f"Команда '{command_name}' запущена в фоновом режиме."
        else:
            # Выполняем команду и получаем вывод (существующая логика)
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