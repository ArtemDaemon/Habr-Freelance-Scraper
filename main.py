import requests as req
from bs4 import BeautifulSoup

if __name__ == '__main__':
    orders = []

    result = req.get("https://freelance.habr.com/tasks")
    soup = BeautifulSoup(result.text, "html.parser")
    orders = soup.findAll("article", class_="task task_list")
