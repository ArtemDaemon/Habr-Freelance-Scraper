import requests as req
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from classes.Order import Order

URLForReq = 'https://freelance.habr.com/tasks'
URLForLink = 'https://freelance.habr.com'

TagArticle = 'article'
TagDiv = 'div'
TagA = 'a'

ClassArticle = 'task task_list'
ClassDivName = 'task__title'
ClassA = 'tags__item_link'
ClassDivLink = 'task__price'


def print_menu():
    params = {}
    settings_dict = {'only_mentioned': 'From those with reviews? Y/N ',
                     'only_with_price': 'With a specified price? Y/N ',
                     'safe_deal': 'With a safe deal? Y/N ',
                     'only_urgent': 'Only urgent orders? Y/N ',
                     'q': 'Search query is '}

    print('Hello, world!')
    for setting in settings_dict:
        answer = input(settings_dict[setting])
        if setting == 'q':
            params[setting] = answer
        elif answer == "Y":
            params[setting] = 'true'

    return params


def load_articles():
    settings = print_menu()
    result = req.get(URLForReq, params=settings)
    status_code = result.status_code
    if status_code != 200:
        print(f'Received status-code - {status_code}')
        return []
    soup = BeautifulSoup(result.text, 'html.parser')
    return soup.findAll(TagArticle, class_=ClassArticle)


def load_orders():
    loaded_orders = []
    articles = load_articles()
    for article in articles:
        name_div = article.find(TagDiv, class_=ClassDivName)
        name = name_div.text
        link = URLForLink + name_div.find(TagA).get('href')
        tags = []
        link_tags = article.findAll(TagA, class_=ClassA)
        for linkTag in link_tags:
            tags.append(linkTag.text)

        price = article.find(TagDiv, class_=ClassDivLink).text

        loaded_orders.append(Order(name, link, tags, price))
    return loaded_orders


if __name__ == '__main__':
    table = Table(title="Task List", show_lines=True)

    table.add_column("Task")
    table.add_column("Price", style="yellow")
    table.add_column("Tags", style="green")
    table.add_column("Link", style="cyan")

    orders = load_orders()
    for order in orders:
        table.add_row(*order.get_list())

    console = Console()
    console.print(table)
    console.print('[green]Done!', style='italic')
