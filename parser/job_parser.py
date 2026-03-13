import requests
from bs4 import BeautifulSoup


def parse_jobs():

    url = "https://realpython.github.io/fake-jobs/"

    response = requests.get(url, timeout=10)

    soup = BeautifulSoup(response.text, "html.parser")

    jobs = []

    for item in soup.select(".card-content"):

        title = item.select_one(".title").text.strip()

        jobs.append({
            "title": title
        })

    return jobs