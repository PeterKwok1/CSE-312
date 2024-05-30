class Category:
    def __init__(self, name):
        self.name = name
        self.ledger = []

    def __str__(self) -> str:
        pass

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
        if self.check_funds(
            amount
        ):  # could just check return of self.withdraw but fcc directions
            self.withdraw(amount, f"Transfer to {partner.name}")
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


food = Category("food")
food.deposit(50, "for veges")
food.withdraw(10, "veges")

clothing = Category("clothing")
clothing.deposit(30, "for shirts")
clothing.withdraw(10, "shirts")

food.transfer(10, clothing)
print(food.ledger, "\n", clothing.ledger)


def create_spend_chart(categories):
    pass
