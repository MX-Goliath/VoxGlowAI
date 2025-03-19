import sys
import json
import numpy as np
import tkinter as tk

from silero_speech import play_tts, stop_tts, is_speaking
play_tts('Инициализация систем')

from vosk import Model, KaldiRecognizer
import pyaudio
import threading
from datetime import datetime
import signal

# Import the modified speech synthesis function

# from G4F_Function import G4F_Function_Main
# from OllamaChat import OllamaChat
# from g4fChat import g4fAnswer
# from Ollama_Function_Calling import Ollama_Funcrions
from Ollama_Functions import Ollama_Function_Main
from video_module import PulsatingSphereWindow  # Ensure this module is correctly implemented



model = Model("model-big")
video_path = "AI_Visualisation.mp4"


# Load commands and settings from JSON file
with open("commands.json", "r", encoding="utf-8") as file:
    commands_data = json.load(file)


# Initialize speech recognition

sample_rate = 16000
recognizer = KaldiRecognizer(model, sample_rate)
p = pyaudio.PyAudio()
stream = p.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, input=True, frames_per_buffer=2048)



# Function to process audio input
stop_audio_thread = False
def audio_processing(window):
    print("Говорите...")
    play_tts('Системы инициализированы')
    
    # Добавляем флаг для отслеживания состояния воспроизведения
    is_tts_active = False
    
    while not stop_audio_thread:
        try:
            data = stream.read(2048, exception_on_overflow=False)
        except Exception as e:
            print(f"Ошибка чтения аудио потока: {e}")
            continue

        # Проверяем, воспроизводится ли сейчас TTS
        is_tts_active = is_speaking()
        
        # Обрабатываем аудио только если TTS не активен
        if not is_tts_active and recognizer.AcceptWaveform(data):
            # Финальный результат готов
            result = json.loads(recognizer.Result()).get('text', '')
            print(f"Распознанный текст: {result}")

            # Проверяем, содержит ли текст имя ассистента
            if any(name.lower() in result.lower() for name in commands_data.get("assistant_name", [])):
                response = Ollama_Function_Main(result)
                # response = G4F_Function_Main(result)
                print(f"Ответ ассистента: {response}")
                stop_tts()  # Останавливаем любое текущее воспроизведение TTS
                play_tts(response)
            else:
                print("Имя ассистента не обнаружено в команде.")
        elif not is_tts_active:
            # Промежуточный результат, речь продолжается (только если TTS не активен)
            partial_result = recognizer.PartialResult()
            partial_text = json.loads(partial_result).get('partial', '')
            if partial_text.strip() != '':
                print(f"Промежуточный результат: {partial_text}")
                stop_tts()  # Останавливаем любое текущее воспроизведение TTS

        # Вычисляем амплитуду для визуализации
        audio_data = np.frombuffer(data, dtype=np.int16).astype(np.float32)
        if len(audio_data) > 0 and np.any(audio_data):
            rms = np.sqrt(np.mean(audio_data ** 2))
            if np.isnan(rms) or rms < 0:
                rms = 0.0
        else:
            rms = 0.0

        amplitude = rms / 3000
        # print(f"Уровень амплитуды: {amplitude}")
        window.set_amplitude(amplitude)



# Initialize the GUI
root = tk.Tk()
window = PulsatingSphereWindow(root, video_path)

# Start audio processing in a separate thread
audio_thread = threading.Thread(target=audio_processing, args=(window,))
audio_thread.daemon = True
audio_thread.start()

# Function to cleanly exit the program
def on_close():
    global stop_audio_thread
    stop_audio_thread = True
    stop_tts()  # Stop any ongoing TTS playback
    stream.stop_stream()
    stream.close()
    p.terminate()
    root.destroy()
    sys.exit()
    
def signal_handler(sig, frame):
    on_close()

signal.signal(signal.SIGINT, signal_handler)

# Start the Tkinter main loop
root.mainloop()
