class Order:
    def __init__(self, name, link, tags, price, safe_deal, urgent):
        self.__name = name
        self.__link = link
        self.__tags = tags
        self.__price = price
        self.__self_deal = safe_deal
        self.__urgent = urgent

    def __str__(self):
        return f"-{self.__name}\n{self.__tags}\n{self.__price}\n{self.__link}\n"

    def get_list(self):
        if self.__self_deal:
            deal_type = "🔐 - Safe deal"
        elif self.__urgent:
            deal_type = "🔥 - Urgent order"
        else:
            deal_type = None
        print_list = (self.__name, deal_type, self.__price, ','.join(self.__tags), self.__link)
        return print_list
