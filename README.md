**VoxGlowAI**

The project is an AI-based voice assistant. A pulsating sphere is used for visualization, whose size changes depending on the sound amplitude. Speech recognition is handled by the local Vosk model, while responses are generated using an LLM model, primarily Ollama. However, there is an option to use other models, such as those from g4f, with limited functionality in terms of function calling. The responses are voiced using Silero. Additionally, there are modules for performing actions such as controlling lighting, computer applications, and more.

For low-performance PCs, it is recommended to use the **Vosk-small** model for your language. Models can be downloaded from the official website: [https://alphacephei.com/vosk/models](https://alphacephei.com/vosk/models). For low-performance PCs, it is also recommended to use **g4f** for generating responses, which will reduce response time for computers without CUDA support or with limited video memory.

To call functions, the `functions` folder contains files with functions and docstrings so that the neural network understands when and what to call. To add your custom functions, create files in that folder similar to the existing ones. A single file can contain multiple functions, and they will be extracted individually.

To use g4f instead of ollama, you need to comment out 
response = Ollama_Function_Main(result)
and uncomment
response = G4F_Function_Main(result)
in the main file.

![image](https://github.com/user-attachments/assets/dc0c3092-d674-4fab-acb6-abb97d4f36c1)


### **Installing Required Python Libraries**

For AMD GPU:
```bash
pip install -r requirements.txt
```

For Nvidia GPU or CPU usage:
```bash
pip install -r requirements_NVIDIA.txt
```

### **Running the Assistant**
To launch the assistant, run:
```bash
python Speech_Recognition.py
```

### **Plans:**
- [ ] Automatic configuration based on user-selected hardware characteristics  
- [ ] Adding cloud speech recognition to reduce PC load  
- [ ] Implementing lightweight speech generation to reduce PC load  
- [x] Function calling using g4f  
- [ ] Adding playback control functionality  
