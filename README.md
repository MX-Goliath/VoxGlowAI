# VoxGlowAI
The project is an AI-based voice assistant. A pulsating sphere, whose size changes based on the sound amplitude, is used for visualization. Speech recognition is handled by the local Vosk model, while the responses are synthesized using Silero. For generating meaningful responses, either a neural network with Ollama is used for local processing, or GPT-4o mini via g4f is employed for non-local computations. There are also modules for performing actions, such as controlling lights, computer applications, and more.

To install the necessary python libraries, use the command:
```bash
pip install ollama vosk pyaudio gigachat sounddevice omegaconf yeelight torch torchvision torchaudio --index-url https://download.pytorch.org/whl/rocm5.6
```

To start the assistant, use the command:
```bash
python Speech_Recognition.py
```
