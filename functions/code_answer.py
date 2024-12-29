def code_answer(query: str) -> None:
    """
    Если вопрос связан с кодом, отправить запрос в специальную нейросеть

    Args:
        content: Текст вопроса пользователя

    Returns:
        str: Возвращает переданный текст
    """
    from g4f.client import Client

    client = Client()
    response = client.chat.completions.create(
        model="claude-3-haiku-20240307",
        messages=[{"role": "user", "content": query}],
        provider="DDG"
        # Add any other necessary parameters
    )
    print(response.choices[0].message.content)
    return response.choices[0].message.content
