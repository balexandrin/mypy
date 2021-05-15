class Square:
    _a = 0
    @property
    def a(self):
        return self._a

    @a.setter
    def a(self, value):
        if value >= 0:
            self._a = value
        else:
            raise ValueError("value must be at least zero")

    @property
    def area(self):
        return self.a ** 2

Sq = Square()
Sq.a = -11
print(Sq.a)
print(Sq.area)