class Rectangle:
    def __init__(self, width, height) -> None:
        self.width = width
        self.height = height

    def __str__(self) -> str:
        return f"Rectangle(width={self.width}, height={self.height})"

    def set_width(self, new_width):
        self.width = new_width

    def set_height(self, new_height):
        self.height = new_height

    def get_area(self):
        return self.width * self.height

    def get_perimeter(self):
        return 2 * self.width + 2 * self.height

    def get_diagonal(self):
        return (self.width**2 + self.height**2) ** 0.5  # hypotenuse formula

    def get_picture(self):
        rect_str = ""
        for line in range(self.height):
            for space in range(self.width):
                pass


a = Rectangle(3, 4)
print(a.get_diagonal())


class Square:
    pass


# how many squares in rectangle without rotating: square side must be less than rect height and width to fit, then integer division height and width and multiply.
