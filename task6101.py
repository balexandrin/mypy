class Rectangle:
    def __init__(self, x, y, width, height):
        self.x = x
        self.y = y
        self.width = width
        self.height = height

    def get_Rectangle(self):
        return 'Rectangle(' + str(self.x) + ',' + str(self.y) + ',' + str(self.width) + ',' + str(self.height) + ')'

fig1 = Rectangle(5,10,50,100)
print(fig1.get_Rectangle())