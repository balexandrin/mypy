class Square:
    def __init__(self, a):
        self.a = a
        self.area = a ** 2

class SquareFactory:
    @staticmethod
    def makeSquare(a):
        return Square(a)
