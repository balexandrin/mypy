import random

"""Родительский класс исключений для всех исключений, используемых в программе, но не являющихся системными"""
class GameException(Exception):
    pass

"""Исключение этого класса выхывается тогда, когда в функцию надо передать параметр типа Cell, но передаваемый параметр 
другого типа. Исключению нужно для отладки программы. Конечный пользователь не должен его видеть, если все написано правильно"""
class noCellException(GameException):
    def __str__(self):
        return 'Аргумент не является ячейкой игрового поля!!!'

"""Ислючение вызывается тогда, когда передаваемый или введеный ползователем параметр имеет значение, выходящее за пределы 
области определения функции. В текущей реализации предполагается, что допустимые значения - целые числа от 1 до 6 включительно"""
class CoordinateValueError(GameException):
    def __str__(self):
        return 'Здесь допустимы только целые числа от 1 до 6!!!'

"""Исключение вызвывается тогда, когда введеный пользователем или передаваемый в функцию параметр имеет тип, отличный от int"""
class CoordinateTypeError(GameException):
    def __str__(self):
        return 'Координаты могут быть только целыми числами!'

"""Исключение вызывается тогда, когда введенное пользователем значение ориентации корабля не является символом 'v' или 'h'"""
class OrientationError(GameException):
    def __str__(self):
        return 'Недопустимая здесь ориентация!!!'

"""Исключение вызывается тогда, когда проверяемый параметр, содержащий количество клеточек = "палуб" корабля выходит за 
границы допустимого"""
class WrongSizeError(GameException):
    def __str__(self):
        return 'Недопустимый размер корабля!!!'

"""Исключение вызывется тогда, когда проверяемый аргумент, переданный в функцию имеет тип, отличный от предусмотренного"""
class ArgumentTypeError(GameException):
    def __str__(self):
        return 'Аргумент неправильного типа!!!'

"""Класс описывает объект, содержащий значения свойств, определяемых правилами игры. В текущей реализации содержитсятолько 
список размеров кораблей"""
class Rules:
    def __init__(self):
        self.ships_types = [3,2,2,1,1,1,1]

"""Класс описывает ячейку игрового поля, как пару значений"""
class Cell:
    def __init__(self, m, n):
        try:
            if not (isinstance(m, int) and isinstance(n, int)):
                raise CoordinateTypeError()
        except CoordinateTypeError as e:
            print(e)
        else:
            self.m = m
            self.n = n

    """Функция проверяет равенство двух ячеек. В текущей реализации программы нигде не используется, написана "на вырост" """
    def __eq__(self, other):
        try:
            if not isinstance(other, Cell):
                raise noCellException()
        except noCellException as e:
            print(e)
            print('Вот этот: ' + str(other) + '. Его класс: ' + str(type(other)))
        else:
            return self.m == other.m and self.n == other.n

    """Функция описыват вид объекта класса при выводе на печать"""
    def __repr__(self):
        return f'({self.m},{self.n})'

    """Очень полезная функция!!! Описывает способ вычесления hash-функции для ячейки, которое и возвращает. Значение 
    hash-функции в программе нигде не используется, но то, что функция определена, делает класс хэшируемым, что, в свою
    очередь, позваляет использовать объекты этого класса, как ключи в словарях"""
    def __hash__(self):
        return self.n * 8 + self.m

"""Класс кораблей. Каждый корабль имеет атрибуты: decks - список ячеек типа Cell, занимаемых кораблем; shadow - список 
ячеек типа Cell, прилегающих к кораблю и находящихся в пределах видимой части поля размером 6х6 ячеек; orientation - 
ориентация корабля на поле. Имеет два допустимых значения h - вдоль верхней и нижней границ монитора и игрового поля,  
v - вдоль левой и правой границ монитора и игрового поля. Любые попытки добавить иные ориентации и гендоры, а так же 
защитить их права, однозначно, признаются психиатрическим заболеванием. Больные будут направлены на принудительное 
лечение; size - размер, он же - количество ячеек в списке decks, до того, как в корабль попадет выстрел. При каждом 
попадании значение size уменьшается на 1. При достижении size == 0 корабль считается потопленым; coordinates - ячейка,
в которой содержится "нос" корабля. От coordinates, в соответствие с ориентацией, размещаются другие ячейки корабля, 
 если таковые имеются"""
class Ship:
    def __init__(self, c, s, o):
            self.decks = []
            self.shadow = []
            self.orientation = o
            self.size = s
            self.coordinates = c
            if self.orientation == 'v':
                for i in range(self.size):
                    self.decks.append(Cell(self.coordinates.m + i, self.coordinates.n))
                for i in range(-1, self.size + 1):
                    for j in range(-1, 2):
                        if not Cell(self.coordinates.m + i, self.coordinates.n + j) in self.decks:
                            if 1 <= self.coordinates.m + i <= 6 and 1 <= self.coordinates.n + j <= 6:
                                self.shadow.append(Cell(self.coordinates.m + i, self.coordinates.n + j))
            if self.orientation == 'h':
                for i in range(self.size):
                    self.decks.append(Cell(self.coordinates.m, self.coordinates.n + i))
                for j in range(-1, self.size + 1):
                    for i in range(-1, 2):
                        if not Cell(self.coordinates.m + i, self.coordinates.n + j) in self.decks:
                            if 1 <= self.coordinates.m + i <= 6 and 1 <= self.coordinates.n + j <= 6:
                                self.shadow.append(Cell(self.coordinates.m + i, self.coordinates.n + j))

"""Класс боевой акватории. В текущей реализации программы, создается два объекта этого класса. Один для человека, второй
для жалкого подобия искуственного интелекта. Атрибуты класса - прекрасны: BA - словарь, который является описанием акватории.
ключи словаря - ячейки типа Cell, значения словаря - числа -2, -1, 0, 1, 2, 4. Значения интерпритируются следующим образом:
-2 - пораженная выстрелом "палуба", -1 - пустая ячека, по которой уже произведет выстрел, 0 - пустая ячека, по которой 
 еще не стреляли, 1 - "палуба" корабля, 2 - тень от корабля, 4 - ячейка за границей видимой части игрового поля; 
 set_of_ships - список объектов типа Ship, размещенных на игровом поле; BASize - размер стороны видимой части игрового поля;
RBASize - размер стороны игрового поля вместе с невидимой его частью. Игровое поле - это квадрат RBASize Х RBASize, 
его видимая часть - это, тоже, квадрат, размером BASize Х BASize. Таким образом, над, под, слева и справа от видимой части 
игрового поля есть еще по одной невидимой строке. По мнению автора, это несколько упращает процедуру размещения кораблей 
в боевой акватории. Это я вам, как автор говорю. Текущая реализация программы "заточена" под размер боевой акватории 6х6
клеточек и семь кораблей на ней. Те, кому не нравится такой размер, пусть молча напишут свою программу и пользуются ей, 
пока никто не видит; ships_on_BA - количество кораблей размещенных на игровом поле и еще не "убитых" противников. При 
размещении кораблей в акватории в начале игры, значение атрибута приростает на 1, при каждом удачном добавлении корабля.
В этой версии программы достигает 7, потому что длина списка ships_types класса Rules равна, как раз, 7. В ходе боя, 
занчение атрибута уменьшается на 1, при каждом потопленном корабле. При ships_on_BA == 0 противоборствующая сторона
признается побежденной; ships_n_shadows - количество ячеек на игровом поле, на которые еще можно разместить корабль. 
До начала размещения кораблей приравнивается "площади" видимой части игрового поля. Далее, уменьшается на число ячеек,
добавленных в списки decks и shadow объектов класса Ship. К вящей радости присутствующих, на поле, размером 6х6, и при 
реализованом наборе кораблей, с размерами [3,2,2,1,1,1,1], легко избежать ситуации, при которой на поле есть N > 1 
свободных ячеек для размещения корабля из 1 < K <= N "палуб", но при этом свободные ячейки разбросаны по полю так, что 
целый корабль в них поместить невозможно. Иначе, алгоритм размещения кораблей был бы невыразимо сложнее. В текущей 
реализации игры достаточно размещать корабли на игровом поле в том порядке, в котором они приведены в списке, по убыванию.
Можно ли добиться ситуации невозможности добавления корабля при наличии свободных ячеек, автор не проверял, желающие 
могут сами доказать возможность или невозможность этого"""
class BattleAquatoria():
    def __init__(self):
        self.BA = {}
        self.set_of_ships = []
        self.BASize = 6
        self.RBASize = 8
        self.ships_on_BA = 0
        self.ships_n_shadows = self.BASize ** 2
        for i in range(self.RBASize):
            for j in range(self.RBASize):
                if 1 <= i <= self.BASize and 1 <= j <= self.BASize:
                    self.BA[Cell(j, i)] = 0
                else:
                    self.BA[Cell(j, i)] = 4

    """Функция, сначала, проверяет тип переданного параметра. Если он есть Ship, то проверяет, весь ли корабль помещается 
    на видимой части игрового поля. Если весь корабль в предлах поля, то проверяет, не заняты ли ячейки, в которые его
    пытаются поместить"""
    def check_ships_location(self, sh):
        try:
            if not isinstance(sh, Ship):
                raise ArgumentTypeError()
        except ArgumentTypeError as e:
            print(e)
            print('Функция check_ships_location!')
            return
        else:
            if (sh.decks[sh.size - 1].m > self.BASize and sh.orientation == 'v') or (sh.decks[sh.size - 1].n > self.BASize and sh.orientation == 'h'):
                return 1
            else:
                occupied = 0
                for i in sh.decks:
                    occupied += self.BA[i]
                return occupied * 10

    """Функция добавлят корабль на игровое поле, если проверка его размещения прошла успешно"""
    def add_ship(self, sh):
        if self.check_ships_location(sh) == 0:
            for i in sh.decks:
                self.BA[i] = 1
                self.ships_n_shadows -= 1
            for i in sh.shadow:
                if self.BA[i] == 0:
                    self.BA[i] = 2
                    self.ships_n_shadows -= 1
            return 0
        else:
            return 1

"""Функция печати боевых акваторий обоих игроков "в строку", слева - человеческое, справа - жалкой пародии на ИИ. 
На вход получает два объекта типа BattleAquatoria. Предполагается, что первый - это человееский, он печатается слева и 
на нем ячейки, занятые кораблями, отображаются черными квадратиками. Второй параметр - это BattleAquatoria машины. Она 
печатается справа, не ней корабли не отображаются"""
def BAprint(MyAq, AiAq):
    try:
        if not (isinstance(MyAq, BattleAquatoria) and isinstance(AiAq, BattleAquatoria)):
            raise ArgumentTypeError()
    except ArgumentTypeError as e:
        print('Аргумент функции печати поля боя может быть только полем боя!')
        print(e)
    else:
        for i in range(MyAq.RBASize - 1):
            st = ''
            strn = ''
            if i == 0:
                for j in range(MyAq.RBASize - 1):
                    strn += str(j)
                st += '|'.join(strn)
                st += ' ' * 10
                strn = ''
                for j in range(AiAq.RBASize - 1):
                    strn += str(j)
                st += '|'.join(strn)
            else:
                strn = str(i)
                for j in range(1, MyAq.RBASize - 1):
                    if MyAq.BA[Cell(i, j)] == 0:
                        strn += 'O'
                    elif MyAq.BA[Cell(i, j)] == 2:
                        strn += 'O'
                    elif MyAq.BA[Cell(i, j)] == 1:
                        strn += '\u25A0'
                    elif MyAq.BA[Cell(i, j)] == -1:
                        strn += 'T'
                    elif MyAq.BA[Cell(i, j)] == -2:
                        strn += 'X'
                st += '|'.join(strn)
                st += ' ' * 10
                strn = str(i)
                for j in range(1, AiAq.RBASize - 1):
                    if AiAq.BA[Cell(i, j)] == 0:
                        strn += 'O'
                    elif AiAq.BA[Cell(i, j)] == 2:
                        strn += 'O'
                    elif AiAq.BA[Cell(i, j)] == 1:
                        strn += 'O'
                    elif AiAq.BA[Cell(i, j)] == -1:
                        strn += 'T'
                    elif AiAq.BA[Cell(i, j)] == -2:
                        strn += 'X'
                st += '|'.join(strn)
            print(st)

"""Функция проверяет параметры для размещения кораблей человком с клавиатуры. Возвращает 0, если все хорошо."""
def input_values_check(input_values):
    if len(input_values) != 3:
        print('Надо ввести ровно две цифры и одну букву!')
        return 1
    try:
        int(input_values[0]) and int(input_values[1])
    except ValueError as e:
        print(CoordinateTypeError())
        return 2
    try:
        if not input_values[2] in ['h', 'v']:
            raise OrientationError()
    except OrientationError as e:
        print(e)
        return 3
    try:
        if not (1 <= int(input_values[0]) <= 6 and 1 <= int(input_values[1]) <= 6):
            raise CoordinateValueError()
    except CoordinateValueError as e:
        print(e)
        return 4
    else:
        return 0

"""Функция проверяет корректность координат для выстрела, вводимых с клавиатуры. Если когда-нибудь автор напишет следующую
версию программы, то в ней эта и предыдущая функции проверки будут заменены на другие. Осталось дождаться, когда автор
напишет следующую версию."""
def shot_coordinates_check(shot_coordinates):
    if len(shot_coordinates) != 2:
        print('Координаты выстрела - это два цлых числа от 1 до 6!')
        return 1
    try:
        int(shot_coordinates[0]) and int(shot_coordinates[1])
    except ValueError as e:
        print(CoordinateTypeError())
        return 2
    try:
        if not (1 <= int(shot_coordinates[0]) <= 6 and 1 <= int(shot_coordinates[1]) <= 6):
            raise CoordinateValueError()
    except CoordinateValueError as e:
        print(e)
        return 4
    else:
        return 0

"""Функция реализует приготовление к битве игрока-человека. Принимает на вход акваторию боя ИИ, исключительно для того,
чтобы можно было пользоваться функцией печати BAprint. В ходе работы функция запрашивает у человека координаты и 
ориентацию, одного за одним, кораблей, подсказывая их размер. Если корабли размещены так, что на следующий не хватает
места, то игровое поле очищается и процесс размещения кораблей начинается снова. Возвращает функция объект класса
BattleAquatoria - заполненное игровое поле человека."""
def myMilitaryPreparations(AiBA):
    Sh_types = Rules()
    ships_on_BA = 0
    while ships_on_BA < len(Sh_types.ships_types):
        MyBA = BattleAquatoria()
        pain_and_despair = False
        for i in Sh_types.ships_types:
            BAprint(MyBA, AiBA)
            add_ok = False
            if MyBA.ships_n_shadows >= i:
                while add_ok == False:
                    print('Размещаем ' + str(i) + '-палубный корабль')
                    print('Введите координаты носа корабля: y - по вертикали, x - по горизонтали и ориентацию v - вертикально, h - гризонтально')
                    input_values = list(input('yxo: '))
                    if input_values_check(input_values) == 0:
                        c = Cell(int(input_values[0]), int(input_values[1]))
                        sh = Ship(c, i, input_values[2])
                        if MyBA.add_ship(sh) == 0:
                            MyBA.set_of_ships.append(sh)
                            ships_on_BA += 1
                            add_ok = True
                            print('Разместили! \n')
                        elif MyBA.add_ship(sh) == 1:
                            print('Таким способом невозможно разместить корабль!')
            else:
                ships_on_BA = 0
                MyBA.set_of_ships.clear()
                MyBA.BA.clear()
                pain_and_despair = True
                print('Доразмещался, стратег!!! Начинай сначала!!!')
            if pain_and_despair == True:
                break
    MyBA.ships_on_BA = ships_on_BA
    return MyBA

"""Фнкция реализует приготовления к битве искуственного интелекта. Делает, почти, тоже самое, что и myMilitaryPreparations(),
исключая запросы на введение данныех с клавиатуры. Вместо этого генерирует координаты и ориентацию корабля при помощи 
генератора случайных чисел."""
def aiMilitaryPreparations():
    Sh_types = Rules()
    ships_on_BA = 0
    while ships_on_BA < len(Sh_types.ships_types):
        AiBA = BattleAquatoria()
        pain_and_despair = False
        for i in Sh_types.ships_types:
            add_ok = False
            if AiBA.ships_n_shadows >= i:
                while add_ok == False:
                    y = random.randint(1, 6)
                    x = random.randint(1, 6)
                    o = random.choice(['h', 'v'])
                    c = Cell(int(y), int(x))
                    sh = Ship(c, i, str(o))
                    a = AiBA.add_ship(sh)
                    if a == 0:
                        AiBA.set_of_ships.append(sh)
                        ships_on_BA += 1
                        add_ok = True
            else:
                ships_on_BA = 0
                AiBA.set_of_ships.clear()
                AiBA.BA.clear()
                pain_and_despair = True
            if pain_and_despair == True:
                break
    AiBA.ships_on_BA = ships_on_BA
    return AiBA

"""Функция реализует, собственно, сражение. Координаты для выстрела от лица человека запрашивает, для выстрела от имени
ИИ - генерирует используя ГСЧ. Определяет режультат выстрела: мимо, ранил, убил или победил. Когда надо передает ход 
противнику или не передает."""
def kill_em_all():
    AiBA = aiMilitaryPreparations()
    MyBA = myMilitaryPreparations(AiBA)
    victory = False
    born_warrior = 0
    while victory == False:
        BAprint(MyBA, AiBA)
        if born_warrior == 0:
            shot_coordinates = list(input('Введите координаты yx на поле противника, по которым хотите выстрелить: '))
            if shot_coordinates_check(shot_coordinates) == 0:
                shot = Cell(int(shot_coordinates[0]), int(shot_coordinates[1]))
                if AiBA.BA[shot] == 0:
                    AiBA.BA[shot] = -1
                    print('Мимо!')
                    born_warrior = (born_warrior + 1) % 2
                    continue
                elif AiBA.BA[shot] == 1:
                    print('Попал!!!')
                    AiBA.BA[shot] = -2
                    for i in AiBA.set_of_ships:
                        if shot in i.decks:
                            i.size -= 1
                            if i.size == 0:
                                print('Убил!!!')
                                AiBA.ships_on_BA -= 1
                                if AiBA.ships_on_BA == 0:
                                    print('Победил!!!')
                                    victory = True
                    continue
                elif AiBA.BA[shot] == 2:
                    AiBA.BA[shot] = -1
                    print('Мимо!')
                    born_warrior = (born_warrior + 1) % 2
                    continue
                elif AiBA.BA[shot] == -1:
                    print('Не надо стрелять по одним координатам много раз!')
                    continue
                elif AiBA.BA[shot] == -2:
                    print('Не надо стрелять по одним координатам много раз!')
                    continue
        elif born_warrior == 1:
            y = random.randint(1, 6)
            x = random.randint(1, 6)
            shot = Cell(y, x)
            print('Чуждая человку сущность выстрелила в: ' + str(y) + ',' + str(x))
            if MyBA.BA[shot] == 0:
                MyBA.BA[shot] = -1
                print('Мимо! Хахаха!')
                born_warrior = (born_warrior + 1) % 2
                continue
            elif MyBA.BA[shot] == 1:
                print('Попала, сволочь!!!')
                MyBA.BA[shot] = -2
                for i in MyBA.set_of_ships:
                    if shot in i.decks:
                        i.size -= 1
                        if i.size == 0:
                            print('Убила, скотина!!!')
                            MyBA.ships_on_BA -= 1
                            if MyBA.ships_on_BA == 0:
                                print('Победил, поганый содомит!!!')
                                BAprint(MyBA, AiBA)
                                victory = True
                continue
            elif MyBA.BA[shot] == 2:
                MyBA.BA[shot] = -1
                print('Мимо! Ы-ы-ы-ы!!!')
                born_warrior = (born_warrior + 1) % 2
                continue
            elif MyBA.BA[shot] == -1:
                print('Сюда эта тупенькая уже стреляла ...')
                continue
            elif MyBA.BA[shot] == -2:
                print('Сюда эта тупенькая уже стреляла ...')
                continue

kill_em_all()

