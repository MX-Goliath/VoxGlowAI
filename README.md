# VoxGlowAI
The project is an AI-based voice assistant. A pulsating sphere, whose size changes based on the sound amplitude, is used for visualization. Speech recognition is handled by the local Vosk model, while the responses are synthesized using Silero. For generating meaningful responses, either a neural network with Ollama is used for local processing, or GPT-4o mini via g4f is employed for non-local computations. There are also modules for performing actions, such as controlling lights, computer applications, and more.
![image](https://github.com/user-attachments/assets/dc0c3092-d674-4fab-acb6-abb97d4f36c1)

To install the necessary python libraries, use the command if you have AMD GPU:
```bash
pip install -r requirements.txt
```

Or if NVIDIA GPU:
```bash
pip install -r requirements_NVIDIA.txt
```

To start the assistant, use the command:
```bash
python Speech_Recognition.py
```
