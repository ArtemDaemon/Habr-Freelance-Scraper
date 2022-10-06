import requests as req
from bs4 import BeautifulSoup
from rich.console import Console
from rich.table import Table
from rich.prompt import Prompt
from classes.Order import Order

URLForReq = 'https://freelance.habr.com/tasks'
URLForLink = 'https://freelance.habr.com'

TagArticle = 'article'
TagDiv = 'div'
TagA = 'a'
TagImg = 'img'

ClassArticle = 'task task_list'
ClassDivName = 'task__title'
ClassA = 'tags__item_link'
ClassDivLink = 'task__price'
ClassImgSafeDeal = 'safe-deal-icon__image'
ClassImgUrgent = 'urgent-badge__image'

console = Console()


def print_menu():
    params = {}
    settings_dict = {'only_mentioned': 'From those with reviews?',
                     'only_with_price': 'With a specified price?',
                     'safe_deal': 'With a safe deal?',
                     'only_urgent': 'Only urgent orders?',
                     'q': 'Search query is '}

    console.print(f'[green]Hello world!', style='italic')
    for setting in settings_dict:
        if setting == 'q':
            answer = Prompt.ask(settings_dict[setting])
            params[setting] = answer
            continue

        answer = Prompt.ask(settings_dict[setting], default="N", choices=["Y", "N"])
        if answer == "Y":
            params[setting] = 'true'

    return params


def load_articles():
    settings = print_menu()
    pages = range(1, 100)
    loaded_articles = []
    for page in pages:
        settings["page"] = str(page)
        result = req.get(URLForReq, params=settings)
        status_code = result.status_code
        if status_code != 200:
            return loaded_articles
        soup = BeautifulSoup(result.text, 'html.parser')
        found_articles = soup.findAll(TagArticle, class_=ClassArticle)
        if len(found_articles) == 0:
            return loaded_articles
        loaded_articles += found_articles

        console.log(f"[yellow]Finish fetching data from page[/yellow] {page}")
    return loaded_articles


def load_orders():
    loaded_orders = []
    articles = load_articles()
    for article in articles:
        safe_deal = False
        urgent = False

        name_div = article.find(TagDiv, class_=ClassDivName)
        name = name_div.text
        link = URLForLink + name_div.find(TagA).get('href')
        tags = []
        link_tags = article.findAll(TagA, class_=ClassA)
        for linkTag in link_tags:
            tags.append(linkTag.text)
        price = article.find(TagDiv, class_=ClassDivLink).text
        if article.find(TagImg, class_=ClassImgSafeDeal):
            safe_deal = True
        elif article.find(TagImg, class_=ClassImgUrgent):
            urgent = True

        loaded_orders.append(Order(name, link, tags, price, safe_deal, urgent))
    return loaded_orders


def create_table():
    console_table = Table(title="Task List", show_lines=True)

    console_table.add_column("Task")
    console_table.add_column("Type", style="yellow")
    console_table.add_column("Price", style="yellow")
    console_table.add_column("Tags", style="green", overflow="fold")
    console_table.add_column("Link", style="cyan", no_wrap=True)

    return console_table


def main():
    table = create_table()

    orders = load_orders()

    text_file = open('readme.txt', 'w', encoding='utf-8')
    for order in orders:
        table.add_row(*order.get_list())
        text_file.write(str(order))
        text_file.write('\n')
    text_file.close()

    console.print(table)
    console.print(f'[green]Done! Displayed {len(orders)} order(s)', style='italic')


if __name__ == '__main__':
    main()
