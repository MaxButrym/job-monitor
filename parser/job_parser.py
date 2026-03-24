import requests # для отправки HTTP-запросов (получаем HTML страницы)
from bs4 import BeautifulSoup # для парсинга HTML и поиска нужных элементов

# Парсит вакансии с тестового сайта и возвращает список словарей с данными о вакансиях
def parse_jobs():
    url = "https://realpython.github.io/fake-jobs/" # тестовый сайт с вакансиями

    try:
        # отправляем GET-запрос к сайту
        response = requests.get(url, timeout=10)
        # проверяем, что ответ успешный (статус 200)
        response.raise_for_status()
    except requests.RequestException as e:
        # если произошла ошибка (нет сети, 404, таймаут и т.д.)
        print(f"Ошибка при запросе: {e}")
        return [] # возвращаем пустой список, чтобы не ломать программу

    soup = BeautifulSoup(response.text, "html.parser") # парсим HTML страницы

    jobs = [] # список для хранения вакансий
    
    # проходим по всем карточкам вакансий
    for item in soup.select(".card-content"):
        # ищем элементы внутри карточки вакансии
        title_tag = item.select_one(".title") # название вакансии
        company_tag = item.select_one(".company") # компания
        location_tag = item.select_one(".location") # локация
        link_tag = item.select_one("a") # ссылка на вакансию
        
        # если какой-то элемент не найден — пропускаем эту вакансию
        if not (title_tag and company_tag and location_tag and link_tag):
            continue
        # извлекаем и очищаем данные
        title = title_tag.text.strip()
        company = company_tag.text.strip()
        location = location_tag.text.strip()
        link = link_tag["href"] # ссылка на вакансию
        
        # добавляем вакансию в список
        jobs.append({
            "title": title,
            "company": company,
            "location": location,
            "link": link,
            "external_id": link,  # уникальный идентификатор (используем ссылку)
            "company_rating": None # пока нет рейтинга компании
        })

    return jobs # возвращаем список всех найденных вакансий