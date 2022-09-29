import requests as req
from bs4 import BeautifulSoup
from classes.Order import Order

URLForReq = "https://freelance.habr.com/tasks"
URLForLink = "https://freelance.habr.com"

TagArticle = "article"
TagDiv = "div"
TagA = "a"

ClassArticle = "task task_list"
ClassDivName = "task__title"
ClassA = "task__item_link"
ClassDivLink = "task__price"


def load_orders():
    loaded_orders = []
    result = req.get(URLForReq)
    status_code = result.status_code
    if status_code != 200:
        print(f"Received status-code - {status_code}")
    soup = BeautifulSoup(result.text, "html.parser")
    articles = soup.findAll(TagArticle, class_=ClassArticle)

    for article in articles:
        name_div = article.find(TagDiv, class_=ClassDivName)
        name = name_div.text
        link = URLForLink + name_div.find(TagA).get("href")
        tags = []
        link_tags = article.findAll(TagA, class_=ClassA)
        for linkTag in link_tags:
            tags.append(linkTag.text)

        price = article.find(TagDiv, class_=ClassDivLink).text

        loaded_orders.append(Order(name, link, tags, price))
    return loaded_orders


if __name__ == '__main__':
    orders = load_orders()
    for order in orders:
        print(order)
