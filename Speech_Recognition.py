# pip install ollama && pip install vosk pyaudio && pip install gigachat && pip install sounddevice && pip install omegaconf && pip install yeelight && pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm5.6


import sys
import json
import numpy as np
import tkinter as tk
from vosk import Model, KaldiRecognizer
import pyaudio
import threading
from datetime import datetime
from tkinter import Button


from silero_speech import *
from OllamaChat import *
from g4fChat import *

# Загрузка JSON файла с командами и настройками
with open("commands.json", "r", encoding="utf-8") as file:
    commands_data = json.load(file)

# Функция для распознавания команды
def recognize_command(text, commands):
    print(commands["commands"])
    for command in commands["commands"]:
        for phrase in command["phrases"]:
            if phrase in text:
                return command["function"]
    return None
# Функции для выполнения команд
def tell_time():
    now = datetime.now()
    return now.strftime("%H:%M")

def tell_date():
    today = datetime.now()
    return today.strftime("%d %B %Y")

# Словарь команд и соответствующих функций
commands_dict = {
    "tell_time": tell_time,
    "tell_date": tell_date,
}

# Инициализация распознавания речи
model = Model("model-small")
sample_rate = 16000
recognizer = KaldiRecognizer(model, sample_rate)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, input=True, frames_per_buffer=8000)

# Функция для обработки аудио
stop_audio_thread = False
def audio_processing(window):
    print("Говорите...")
    silero_nuero_speech('Системы инициализированы')
    while not stop_audio_thread:
        try:
            data = stream.read(8000, exception_on_overflow=False)
        except Exception as e:
            print(f"Ошибка чтения аудио потока: {e}")
            continue

        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result()).get('text', '')
            print(f"Распознанный текст: {result}")
            command_name = recognize_command(result, commands_data)
            # print(f"Список команд: {commands_data[command_name]}")

            if command_name in commands_dict:
                response_function = commands_dict[command_name]
                response = response_function()
                print("Команда выполнена")
                silero_nuero_speech(response)
            else:
                print("Команда не распознана")
                print(f"Список имен ассистента: {commands_data['assistant_name']}")
                if any(name.lower() in result for name in commands_data["assistant_name"]):
                    # response = OllamaChat(result)
                    response = g4fAnswer(result)
                    print(response)
                    silero_nuero_speech(response)

        audio_data = np.frombuffer(data, dtype=np.int16).astype(np.float32)
        if len(audio_data) > 0 and np.any(audio_data):
            rms = np.sqrt(np.mean(audio_data ** 2))
            if np.isnan(rms) or rms < 0:
                rms = 0.0
        else:
            rms = 0.0

        amplitude = rms / 3000
        print(f"Уровень амплитуды: {amplitude}")
        window.set_amplitude(amplitude)

# Функция для запуска окна и аудио
root = tk.Tk()
video_path = "original-edddd691de851d37c06bf51df78011af.mp4"
from video_module import PulsatingSphereWindow  # Импорт функции из отдельного файла
window = PulsatingSphereWindow(root, video_path)

# Запуск аудиообработки в отдельном потоке
audio_thread = threading.Thread(target=audio_processing, args=(window,))
audio_thread.daemon = True
audio_thread.start()

# Функция для завершения работы
def on_close():
    global stop_audio_thread
    stop_audio_thread = True
    root.destroy()

root.protocol("WM_DELETE_WINDOW", on_close)

# Запуск основного цикла Tkinter
root.mainloop()
