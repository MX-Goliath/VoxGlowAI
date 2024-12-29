def smart_answer(query: str) -> None:
    """
    Если вопрос сложный, отправить запрос в умную нейросеть

    Args:
        content: Текст вопроса пользователя

    Returns:
        str: Возвращает переданный текст
    """
    from g4f.client import Client

    client = Client()
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[{"role": "user", "content": query}],
        provider="DDG"
        # Add any other necessary parameters
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content
