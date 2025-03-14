from duckduckgo_search import DDGS
from bs4 import BeautifulSoup
import requests
import re

def web_search(query: str) -> str:
    """
    Выполняет поиск в интернете через DuckDuckGo и возвращает текст с первых трех результатов.

    Args:
        query: Поисковый запрос

    Returns:
        str: Объединенный текст из первых трех результатов поиска
    """
    try:
        # Инициализация поиска
        with DDGS() as ddgs:
            # Получаем первые 3 результата
            search_results = list(ddgs.text(query, max_results=3))
            if not search_results:
                return "К сожалению, не удалось найти информацию по вашему запросу."
        
        combined_text = []
        
        for result in search_results:
            try:
                # Получаем URL из результата
                url = result.get('href') or result.get('url')
                if not url:
                    continue
                
                # Получаем содержимое страницы
                response = requests.get(url, timeout=5)
                response.raise_for_status()
                
                # Парсим HTML
                soup = BeautifulSoup(response.text, 'html.parser')
                
                # Удаляем ненужные элементы
                for tag in soup(['script', 'style', 'header', 'footer', 'nav']):
                    tag.decompose()
                
                # Получаем текст
                text = soup.get_text()
                
                # Очищаем текст
                text = re.sub(r'\s+', ' ', text).strip()
                text = re.sub(r'[^\w\s.,!?-]', '', text)
                
                # Добавляем заголовок из результата поиска
                title = result.get('title', '')
                snippet = result.get('body', '')
                
                # Формируем текст результата
                result_text = f"{title}\n{snippet}\n\n{text[:1000]}..."
                
                combined_text.append(result_text)
                
            except Exception as e:
                print(f"Ошибка при обработке результата: {e}")
                continue
        
        # Объединяем результаты
        if combined_text:
            final_text = "\n\n---\n\n".join(combined_text)
            return f"Результаты поиска по запросу '{query}':\n\n{final_text}"
        else:
            return "К сожалению, не удалось найти информацию по вашему запросу."
            
    except Exception as e:
        return f"Произошла ошибка при выполнении поиска: {str(e)}" 
    

# print(web_search("Тахионы"))