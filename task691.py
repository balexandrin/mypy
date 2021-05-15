from Figures691 import Rectangle, Square, Circle

rect1 = Rectangle(3, 4)
rect2 = Rectangle(12 ,5)
square1 = Square(5)
square2 = Square(10)
circle1 = Circle(5)
circle2 = Circle(10)

figures = [rect1, rect2, square1, square2, circle1, circle2]

for figure in figures:
    if isinstance(figure, Rectangle):
        print(figure.get_area())
    elif isinstance(figure, Square):
        print(figure.get_area_square())
    elif isinstance(figure, Circle):
        print(figure.get_area_circle())