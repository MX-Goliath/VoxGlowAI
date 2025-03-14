import torch
import sounddevice as sd
import time
import threading

# Pre-configured parameters
language = 'ru'
model_id = 'v4_ru'
sample_rate = 24000
put_accent = True
put_yoo = True
device = torch.device('cpu')

# Load the TTS model
model, _ = torch.hub.load(repo_or_dir='snakers4/silero-models',
                          model='silero_tts',
                          language=language,
                          speaker=model_id)
model.to(device)

# aidar, baya, kseniya, xenia, eugene, random
def silero_nuero_speech(text, speaker='baya', stop_event=None):
    """
    Function for speech synthesis using given text and speaker.

    Parameters:
    text (str): Text to synthesize.
    speaker (str): Speaker identifier.
    stop_event (threading.Event): Event to signal playback should stop.
    """
    audio = model.apply_tts(text=text,
                            speaker=speaker,
                            sample_rate=sample_rate,
                            put_accent=put_accent,
                            put_yo=put_yoo)
    # Play audio in chunks to allow interruptiozn
    chunk_size = 1024
    total_frames = len(audio)
    current_frame = 0

    def callback(outdata, frames, time_info, status):
        nonlocal current_frame
        if stop_event and stop_event.is_set():
            raise sd.CallbackStop()
        end_frame = current_frame + frames
        if end_frame > total_frames:
            end_frame = total_frames
        outdata[:end_frame - current_frame, 0] = audio[current_frame:end_frame]
        if end_frame - current_frame < frames:
            outdata[end_frame - current_frame:] = 0
            raise sd.CallbackStop()
        current_frame = end_frame

    try:
        with sd.OutputStream(samplerate=sample_rate, channels=1, callback=callback):
            while not stop_event or not stop_event.is_set():
                time.sleep(0.1)
    except sd.CallbackStop:
        pass
    except Exception as e:
        print(f"Error during playback: {e}")
    sd.stop()


# Variables to control TTS playback
tts_playback_thread = None
stop_tts_playback = threading.Event()

# Function to play TTS in a separate thread
def play_tts(text):
    global stop_tts_playback, tts_playback_thread, _is_speaking
    _is_speaking = True
    stop_tts_playback.clear()
    def tts():
        silero_nuero_speech(text, stop_event=stop_tts_playback)
    tts_playback_thread = threading.Thread(target=tts)
    tts_playback_thread.start()
    _is_speaking = False

# Function to stop TTS playback
def stop_tts():
    global stop_tts_playback, tts_playback_thread
    if tts_playback_thread and tts_playback_thread.is_alive():
        stop_tts_playback.set()
        tts_playback_thread.join()

# Add a new function to check if TTS is speaking
def is_speaking():
    global _is_speaking
    return _is_speaking

# play_tts('Можно купить студию через года полтора, когда будет достаточный запас помимо первого взноса и сдавать ее, платить по 50000 в месяц с платой от арендаторов и жить на съемной. Тогда будет возможность использовать свободные оставшиеся деньги')
