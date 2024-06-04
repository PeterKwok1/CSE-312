import copy
import random


class Hat:
    def __init__(self, **kwargs) -> None:
        # dict to list
        self.contents = []
        for ball, number in kwargs.items():  # similar to enumerate or a list of lists.
            for _ in range(number):
                self.contents.append(ball)


def experiment(hat, expected_balls, num_balls_drawn, num_experiments):
    pass


# copy.deepcopy(x)
# list to dict
# list to unique list: https://www.geeksforgeeks.org/python-get-unique-values-list/
# .dict() or increment dict value over list

hat_test = Hat(red=1, green=2, blue=3)
print(hat_test.contents)

test = [[1, 2, 3], [4, 5, 6]]
for a, b, c in test:
    print(a, b, c)
