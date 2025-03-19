import threading
import time
from datetime import datetime, timedelta

class TimerManager:
    def __init__(self, notify_callback):
        """
        Инициализация TimerManager.

        :param notify_callback: Функция обратного вызова для уведомления пользователя.
        """
        self.timer_thread = None
        self.end_time = None
        self.notify_callback = notify_callback
        self.lock = threading.Lock()

    def set_timer(self, duration_seconds):
        """
        Устанавливает таймер на заданное количество секунд.

        :param duration_seconds: Продолжительность таймера в секундах.
        :return: Сообщение о результате установки таймера.
        """
        with self.lock:
            try:
                # Преобразуем duration_seconds в целое число
                duration_seconds = int(duration_seconds)
                if duration_seconds <= 0:
                    return "Пожалуйста, укажите положительное время для таймера."
            except ValueError:
                return "Неверный формат времени. Пожалуйста, укажите время в секундах."

            if self.timer_thread and self.timer_thread.is_alive():
                self.cancel_timer()

            self.end_time = datetime.now() + timedelta(seconds=duration_seconds)
            self.timer_thread = threading.Thread(target=self._run_timer)
            self.timer_thread.start()
            return f"Таймер установлен на {duration_seconds} секунд."

    def _run_timer(self):
        """
        Фоновый поток для отслеживания таймера.
        """
        while True:
            with self.lock:
                if not self.end_time:
                    break
                remaining = (self.end_time - datetime.now()).total_seconds()
                if remaining <= 0:
                    self.notify_callback("Таймер завершен!")
                    self.end_time = None
                    break
            time.sleep(1)

    def get_timer(self):
        """
        Возвращает оставшееся время таймера.

        :return: Сообщение с оставшимся временем или уведомление, что таймер не установлен.
        """
        with self.lock:
            if self.end_time:
                remaining = self.end_time - datetime.now()
                if remaining.total_seconds() > 0:
                    minutes, seconds = divmod(int(remaining.total_seconds()), 60)
                    return f"Осталось {minutes} минут и {seconds} секунд."
            return "Таймер не установлен."

    def cancel_timer(self):
        """
        Отменяет текущий таймер.

        :return: Сообщение о результате отмены таймера.
        """
        with self.lock:
            if self.timer_thread and self.timer_thread.is_alive():
                self.end_time = None
                self.timer_thread.join()
                self.timer_thread = None
                return "Таймер отменен."
            return "Таймер не установлен."

# Глобальный объект таймер-менеджера
timer_manager = None

def initialize_timer_manager(notify_callback):
    global timer_manager
    if timer_manager is None:
        timer_manager = TimerManager(notify_callback)
    return timer_manager

def set_timer(duration_seconds):
    if timer_manager:
        return timer_manager.set_timer(duration_seconds)
    return "Таймер менеджер не инициализирован."

def get_timer():
    if timer_manager:
        return timer_manager.get_timer()
    return "Таймер менеджер не инициализирован."

def cancel_timer():
    if timer_manager:
        return timer_manager.cancel_timer()
    return "Таймер менеджер не инициализирован."
