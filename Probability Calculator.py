import copy
import random


class Hat:
    def __init__(self, **kwargs) -> None:
        # dict to list
        self.contents = []
        for ball, number in kwargs.items():  # similar to enumerate or a list of lists.
            for _ in range(number):
                self.contents.append(ball)

    def draw(self, number_to_draw):
        contents_copy = copy.deepcopy(self.contents)
        result = []
        for _ in range(number_to_draw):
            if len(contents_copy):
                index = random.randint(0, len(contents_copy) - 1)
                result.append(contents_copy.pop(index))
        return result


def experiment(hat, expected_balls, num_balls_drawn, num_experiments):
    pass


# copy.deepcopy(x)
# list to dict
# list to unique list: https://www.geeksforgeeks.org/python-get-unique-values-list/
# .dict() or increment dict value over list

hat_test = Hat(red=1, green=1, blue=1)
print(hat_test.draw(5))
