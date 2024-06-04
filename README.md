
# Polygon Area Calculator 

Rectangle class with set_width, set_height, get_area, get_perimeter, get_diagonal, get_picture, and get_amount_inside methods. 

Rectangle.get_picture() prints the rectangle
Rectangle.get_amount_inside() takes another rectangle and returns the number of times it fits inside this one without rotating it.

Square subclass with additional set_side method. 

Example
```
rect = Rectangle(10, 5)
print(rect.get_area())
rect.set_height(3)
print(rect.get_perimeter())
print(rect)
print(rect.get_picture())

sq = Square(9)
print(sq.get_area())
sq.set_side(4)
print(sq.get_diagonal())
print(sq)
print(sq.get_picture())

rect.set_height(8)
rect.set_width(16)
print(rect.get_amount_inside(sq))

<!-- Returns -->
50
26
Rectangle(width=10, height=3)
**********
**********
**********

81
5.656854249492381
Square(side=4)
****
****
****
****

8
```

For the purpose of reviewing python to follow cse 312. 




