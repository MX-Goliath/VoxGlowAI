import ollama

def OllamaChat(message):
    response = ollama.chat(model='phi3.5:latest', messages=[
    {
        'role': 'user',
        'content': f'Your name is Caroline, you are a voice assistant - a girl. Answer only in Russian. Respond to this user message briefly:{message}',
    },
    ])
    return response['message']['content']

# response = OllamaChat('Привет')
# print(response)

