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
        if self.width > 50 or self.height > 50:
            return "Too big for picture."
        rect_str = ""
        for line in range(self.height):
            for space in range(self.width):
                rect_str += "*"
            rect_str += "\n"  # remove last \n ?
        return rect_str

    def get_amount_inside(self, shape):
        # square side must be less than rect width and height to fit. integer division height and width and multiply.
        width_fit = self.width // shape.width
        height_fit = self.height // shape.height
        return width_fit * height_fit


# inheritance: https://www.w3schools.com/python/python_inheritance.asp
class Square(Rectangle):
    def __init__(self, side) -> None:
        super().__init__(side, side)

    def __str__(self) -> str:
        return f"Square(side={self.width})"

    def set_side(self, side):
        self.width = side
        self.height = side

    def set_width(self, side):
        self.width = side
        self.height = side

    def set_height(self, side):
        self.width = side
        self.height = side


b = Square(3)
b.set_side(4)
print(b.width, b.height)
