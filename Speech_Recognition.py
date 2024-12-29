import sys
import json
import numpy as np
import tkinter as tk
from vosk import Model, KaldiRecognizer
import pyaudio
import threading
from datetime import datetime

# Import the modified speech synthesis function
from silero_speech import silero_nuero_speech
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
stream = p.open(format=pyaudio.paInt16, channels=1, rate=sample_rate, input=True, frames_per_buffer=8000)

# Variables to control TTS playback
tts_playback_thread = None
stop_tts_playback = threading.Event()

# Function to play TTS in a separate thread
def play_tts(text):
    global stop_tts_playback, tts_playback_thread
    stop_tts_playback.clear()
    def tts():
        silero_nuero_speech(text, stop_event=stop_tts_playback)
    tts_playback_thread = threading.Thread(target=tts)
    tts_playback_thread.start()

# Function to stop TTS playback
def stop_tts():
    global stop_tts_playback, tts_playback_thread
    if tts_playback_thread and tts_playback_thread.is_alive():
        stop_tts_playback.set()
        tts_playback_thread.join()

# Function to process audio input
stop_audio_thread = False
def audio_processing(window):
    print("Говорите...")
    play_tts('Системы инициализированы')
    while not stop_audio_thread:
        try:
            data = stream.read(2048, exception_on_overflow=False)
        except Exception as e:
            print(f"Ошибка чтения аудио потока: {e}")
            continue

        if recognizer.AcceptWaveform(data):
            # Финальный результат готов
            result = json.loads(recognizer.Result()).get('text', '')
            print(f"Распознанный текст: {result}")

            # Проверяем, содержит ли текст имя ассистента
            if any(name.lower() in result.lower() for name in commands_data.get("assistant_name", [])):
                response = Ollama_Function_Main(result)
                print(f"Ответ ассистента: {response}")
                stop_tts()  # Останавливаем любое текущее воспроизведение TTS
                play_tts(response)
            else:
                print("Имя ассистента не обнаружено в команде.")
        else:
            # Промежуточный результат, речь продолжается
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

root.protocol("WM_DELETE_WINDOW", on_close)

# Start the Tkinter main loop
root.mainloop()
