# Установить omegaconf
import torch
import sounddevice as sd
import time

# Предварительная настройка параметров
language = 'ru'
model_id = 'ru_v3'
sample_rate = 24000
put_accent = True
put_yoo = True
device = torch.device('cpu')

# Загрузка модели
model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                          model='silero_tts',
                          language=language,
                          speaker=model_id)
model.to(device)

def silero_nuero_speech(text, speaker='baya'):
    """
    Функция для синтеза речи с использованием заданного текста и диктора.
    
    Параметры:
    text (str): Текст для синтеза.
    speaker (str): Идентификатор диктора.
    """
    audio = model.apply_tts(text=text,
                            speaker=speaker,
                            sample_rate=sample_rate,
                            put_accent=put_accent,
                            put_yo=put_yoo)
    sd.play(audio, sample_rate * 1.05)
    time.sleep((len(audio) / sample_rate) + 0.5)
    sd.stop()

# Пример использования функции с указанием диктора
# silero_nuero_speech('Да, сэр', 'aidar') # `speaker` должен быть одним из: aidar, baya, kseniya, xenia, random
