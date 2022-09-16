import requests as req
from bs4 import BeautifulSoup
from classes.Order import Order

URLForReq = "https://freelance.habr.com/tasks?q=python"
URLForLink = "https://freelance.habr.com"


if __name__ == '__main__':
    orders = []

    result = req.get(URLForReq)
    soup = BeautifulSoup(result.text, "html.parser")
    articles = soup.findAll("article", class_="task task_list")

    for article in articles:
        nameDiv = article.find("div", class_="task__title")
        name = nameDiv.text
        link = URLForLink + nameDiv.find("a").get("href")
        tags = []
        linkTags = article.findAll("a", class_="tags__item_link")
        for linkTag in linkTags:
            tags.append(linkTag.text)

        price = article.find("div", class_="task__price").text

        orders.append(Order(name, link, tags, price))

    for order in orders:
        print(order)
