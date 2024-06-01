class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def __str__(self) -> str:
        entries_str = ""

        # add title
        padding = "*" * int((30 - len(self.name)) / 2)
        title = f"{padding}{self.name}{padding}\n"
        entries_str += title

        # add entries
        for entry in self.ledger:
            description = entry["description"][:23]
            amount = f"{entry['amount']:.2f}"  # .2f = round float to two decimal places
            line = f"{description}{amount:>{30 - len(description)}}\n"
            entries_str += line

        # add net

        net = f"Total: {self.get_balance()}"
        entries_str += net

        return entries_str

    def deposit(self, amount, description=""):
        entry = {"amount": amount, "description": description}
        self.ledger.append(entry)

    def withdraw(self, amount, description=""):
        if self.check_funds(amount):
            entry = {"amount": 0 - amount, "description": description}
            self.ledger.append(entry)
            return True
        return False

    def get_balance(self):
        ledger_amounts = [entry["amount"] for entry in self.ledger]
        net = sum(ledger_amounts)
        return net

    def transfer(self, amount, partner):
        if self.withdraw(amount, f"Transfer to {partner.name}"):
            partner.deposit(amount, f"Transfer from {self.name}")
            return True
        return False

    def check_funds(self, amount):
        ledger_amounts = [entry["amount"] for entry in self.ledger]
        net = sum(ledger_amounts)
        if amount > net:
            return False
        else:
            return True


def create_spend_chart(categories):
    bar_str = ""

    # title
    title = "Percentage spent by category\n"
    bar_str += title

    # chart
    # percentage of withdrawls from total withdrawls
    # their design considers withdrawls as a result of transfers as spent money

    # values
    withdrawls = []
    total_withdrawls = 0

    for category in categories:
        category_withdrawls = 0

        for entry in category.ledger:
            if entry["amount"] < 0:
                category_withdrawls += entry["amount"]

        withdrawls.append((category.name, category_withdrawls))
        total_withdrawls += category_withdrawls

    withdrawl_percentages = [  # convert to %
        (category[0], category[1] / total_withdrawls * 100) for category in withdrawls
    ]

    # y axis
    y_axis = list(range(100, -1, -10))

    # add axis + values
    # nested for loop
    # round down and compare x // y > 0
    for y in y_axis:
        bar_str += f'{str(y) + "|":>4}'
        for category in withdrawl_percentages:
            if (
                y != 0
            ):  # they made 0 a value on the chart and not the origin. they may want to capture 1-9 since they're rounding down.
                if category[1] // y > 0:
                    bar_str += " o "
                else:
                    bar_str += " " * 3
            elif y == 0:
                bar_str += " o "
        bar_str += " \n"

    # divider
    bar_str += f'{" " * 4}{"-" * 3 * len(withdrawl_percentages) + "-"}\n'

    # x axis
    number_of_lines = max([len(category[0]) for category in withdrawl_percentages])
    for line_number in range(number_of_lines):
        bar_str += f'{" ":>4}'
        for category in withdrawl_percentages:
            if line_number < len(category[0]):
                bar_str += f" {category[0][line_number]} "
            else:
                bar_str += " " * 3
        if line_number < number_of_lines - 1:
            bar_str += " \n"
        else:
            bar_str += " "

    return bar_str


# ex
food = Category("food")
food.deposit(50, "for veges")
food.withdraw(10, "veges")

clothing = Category("clothing")
clothing.deposit(30, "for shirts")
clothing.withdraw(10, "shirts")

food.transfer(10, clothing)

print("\n")
print(food)
print(clothing)
print("\n")
print(create_spend_chart([food, clothing]))
