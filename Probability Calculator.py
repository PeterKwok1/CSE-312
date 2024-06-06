import copy
import random


# dict to list for dict with int values
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
        # fcc test needed this to pass even though the code below includes this case.
        if number_to_draw > len(self.contents):
            result = copy.deepcopy(self.contents)
            self.contents = []
            return result

        result = []
        for _ in range(number_to_draw):
            if len(self.contents):  # could make inline, but prefer readability
                index = random.randint(0, len(self.contents) - 1)
                pick = self.contents.pop(index)
                result.append(pick)
        return result


def experiment(hat, expected_balls, num_balls_drawn, num_experiments):
    expected_result = dict_to_list(expected_balls)

    success_count = 0

    for _ in range(num_experiments):
        result = copy.deepcopy(hat).draw(num_balls_drawn)

        is_subset = True
        for ball in expected_result:
            if ball in result:
                result.remove(ball)
            else:
                is_subset = False
                break

        if is_subset:
            success_count += 1

    approx_probability = success_count / num_experiments
    return approx_probability


# hat_test = Hat(red=1, green=1)
# expected_balls_test = {"red": 1}
# num_balls_drawn_test = 1
# num_experiments_test = 100
# print(
#     experiment(
#         hat_test, expected_balls_test, num_balls_drawn_test, num_experiments_test
#     )
# )
