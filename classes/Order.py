class Order:
    def __init__(self, name, link, tags, price):
        self.name = name
        self.link = link
        self.tags = tags
        self.price = price

    def __str__(self):
        return f"-{self.name}\n{self.tags}\n{self.price}\n{self.link}\n"
