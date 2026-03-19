import requests
from bs4 import BeautifulSoup


def parse_jobs():

    url = "https://realpython.github.io/fake-jobs/"

    response = requests.get(url, timeout=10)

    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    for i, item in enumerate(soup.select(".card-content")):
        title = item.select_one(".title").text.strip()

        company = item.select_one(".company").text.strip()

        location = item.select_one(".location").text.strip()

        link = item.select_one("a")["href"]
        unique_link = f"{link}_{i}"
        
        jobs.append({
            "title": title,
            "company": company,
            "location": location,
            "link": link,
            "external_id": f"{link}_{i}",  # 👈 НОВОЕ ПОЛЕ
            "company_rating": None
        })

    return jobs