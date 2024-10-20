from g4f.client import Client

def g4fAnswer(message):
    client = Client()
    response = client.chat.completions.create(
        model="gpt4o-mini",
        messages=[{"role": "user", "content": "Тебя зовут Кэролайн, ты голосовой помощник - девушка. Отвечайте только на русском языке. Все числа пиши словами. Формулы все так же пиши словами. " +message}],
        provider="DDG"
    )
    return response.choices[0].message.content
    # print(response.choices[0].message.content)

# response = g4fAnswer('Что ты можешь?')
# print(response)
