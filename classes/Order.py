class Order:
    def __init__(self, name, link, tags, price):
        self.__name = name
        self.__link = link
        self.__tags = tags
        self.__price = price

    def __str__(self):
        return f"\n-{self.__name}\n{self.__tags}\n{self.__price}\n{self.__link}\n"
