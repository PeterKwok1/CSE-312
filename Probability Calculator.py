import copy
import random


# dict to list for int values
def dict_to_list(dict_obj):
    list = []
    for key, value in dict_obj.items():  # similar to enumerate or a list of lists.
        for _ in range(value):
            list.append(key)
    return list


class Hat:
    def __init__(self, **kwargs) -> None:
        self.contents = dict_to_list(kwargs)

    def draw(self, number_to_draw):
        contents_copy = copy.deepcopy(self.contents)
        result = []
        for _ in range(number_to_draw):
            if len(contents_copy):  # could make inline, but prefer readability
                index = random.randint(0, len(contents_copy) - 1)
                pick = contents_copy.pop(index)
                result.append(pick)
        return result


def experiment(hat, expected_balls, num_balls_drawn, num_experiments):
    expected_result = dict_to_list(expected_balls)
    success_count = 0

    for _ in range(num_experiments):
        result = hat.draw(num_balls_drawn)
        if (
            result == expected_result
        ):  # issue is the lists are in different orders. options are to convert to dict or sort before compare
            success_count += 1

    approx_probability = success_count / num_experiments
    return approx_probability


hat_test = Hat(red=1, green=2, blue=3)
expected_balls_test = {"red": 1, "green": 1}
num_balls_drawn_test = 3
num_experiments_test = 100
print(
    experiment(
        hat_test, expected_balls_test, num_balls_drawn_test, num_experiments_test
    )
)

# copy.deepcopy(x)
# list to dict
# list to unique list: https://www.geeksforgeeks.org/python-get-unique-values-list/
# .dict() or increment dict value over list
