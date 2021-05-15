import random

#Класс кораблей. x - номер "первой" клеточки, занятой кораблем в строке. y - номер "первой" клеточки, занятой кораблем в столбце.
#size - количество клеточек на игровом поле, которое занимает корабль. То же, что "количество палуб"
#orientation - ориентация коробля, у которого больше одной "палубы" вдоль осей. 'h' - горизонтальное, корабль расположен бортом
#вдоль "горизонтальной" оси. 'v' - вертикальная, корабль расположен вдоль "вертикальной" оси. У кораблей неразличимы нос и корма,
#левый борт и правый борт. Все клеточки, занятые кораблем равнозначны.
class Ship:
    def __init__(self, size):
        self.x = 0
        self.y = 0
        self.size = int(size)
        self.orientation = None
        self.holes = int(0)
        self.decks = []
        for i in range(self.size):
            self.decks.append([])

    def setX(self, x):
        try:
            if not (1 <= int(x) <= 6):
                raise ValueError('Х вне допустимого диапозона!')
        except:
            return 1
        else:
            self.x = x
            return 0

    def setY(self, y):
        try:
            if not (1 <= int(y) <= 6):
                raise ValueError('Y вне допустимого диапозона!')
        except:
            return 1
        else:
            self.y = y
            return 0

    def setOr(self, Ornt):
        try:
            if not (Ornt in ['v', 'h']):
                raise ValueError('Ориентация игрока вне допустимого диапозона!')
        except:
            return 1
        else:
            self.orientation = Ornt
            return 0

    def setHoles(self):
        self.holes += 1

    def getX(self):
        return int(self.x)

    def getY(self):
        return int(self.y)

    def getOrientation(self):
        return self.orientation

    def getSize(self):
        return int(self.size)

    def getHoles(self):
        return self.holes

# Класс, описывающий поля боя. Поле боя - это квадратная таблица размером 9х9. И это не смтря на то, что в игре для игроков доступно
# поле размером 6х6. Дополнительные строки и столбцы добавлены по двум причинам. Во-первых, строки и колонки номер ноль и семь добавлены
# для того, чтобы обеспечить минимальное расстояние между кораблями в одну клетку. Введение нулевой и седьмой строки и столбца
# упрощают технологию этого контроля. В строке номер восемь и в столбце номер восемь отображатеся "тень", или проекция,
# клеточек занятых как самим короблем, так и прилегающих к нему клеточек, которые должны быть свободны,
# согласно требованию ТЗ, п.6 "Корабли должны находится на расстоянии минимум одна клетка друг от друга".
# Клетки таблицы с координатами (0,0) (7,7) (7,8) (8,7) (8,8) не используются никак.
# Во-вторых, дополнительные строки и столбцы с неиспользуемыми клетками добавлены на зло. Они должны раздражать тех,
# кто "не понимает, зачем они нужныи" и тех, кому "не проще ли сделать по-другому!!!"
# То игровое поле, которое визуализируется для игрока - это подмножество поля боя и шаблона из заголовков строк и столбцов,
# вертикальных и горизонтальных черточек, образующих ячейки таблицы.
class BattleAquatoria:
    sizeBA = 6
    sizeBA += 1
    RsizeBA = sizeBA + 1
    shipsAndShadows = 0
    def __init__(self): # Конструктор класса, который формирует "чистое" поле боя, на котором нет ничего, ни одного корабля.
        self.BA = []
        for i in range(self.RsizeBA):
            str = [0] * self.RsizeBA
            self.BA.append(str)

    def getSizeBA(self):
        return self.sizeBA

    def setShipsAndShadows(self, delta):
        self.shipsAndShadows += delta

    def getShipsAndShadows(self):
        return self.shipsAndShadows

    def setXY(self, shot, num):
        self.BA[int(shot[1])][int(shot[0])] = int(num)

    def checkShipLocation(self, s, x, y, o):
        if self.shipsAndShadows >= (self.sizeBA - 1) ** 2:
            return 2
        if o == 'v':
            if int(y) + int(s) > self.sizeBA:
                return 1
            for i in range(int(y) - int(1), int(y) + int(s) + 1):
                for j in range(int(x) - int(1), int(x) + int(2)):
                    if self.BA[i][j] == 1:
                        return 1
        elif o == 'h':
            if int(x) + int(s) > self.sizeBA:
                return 1
            for i in range(int(x) - int(1), int(x) + int(s) + 1):
                for j in range(int(y) - int(1), int(y) + 2):
                    if self.BA[j][i] == 1:
                        return 1
        return 0

    def addShip(self, ship): # Функция, которая принимает объект - корабль, проверяет возможность его размещения на поле боя.
        # К этому моменту уже должна быть проверена совместимость текущей обстановки на поле боя, параметров нового корабля и
        # требований ТЗ.
        d = 0
        if ship.orientation == 'v':
            for i in range(ship.getY() - int(1), ship.getY() + ship.getSize() + 1):
                for j in range(ship.getX() - int(1), ship.getX() + 2):
                    if  1 <= i <= 6 and 1 <= j <= 6 and self.BA[i][j] != 2:
                        self.BA[i][j] = 2
                        self.setShipsAndShadows(1)

            print('ship.getX() = ' + str(ship.getX()))
            print('ship.getY() = ' + str(ship.getY()))
            print('ship.getSize() = ' + str(ship.getSize()))
            for i in range(ship.getY(), ship.getY() + ship.getSize()):
                self.BA[i][ship.getX()] = 1
#                print('ship.getSize() = ' + str(ship.getSize()))
#                print('ship.getX() = ' + str(ship.getX()))
#                print('ship.getY() = ' + str(ship.getY()))
                print('d = ' + str(d))
                print('i = ' + str(i))
                ship.decks[d].append(i)
                ship.decks[d].append(ship.getX())
                d += 1
        elif ship.orientation == 'h':
            for i in range(ship.getX() - int(1), ship.getX() + ship.getSize() + 1):
                for j in range(ship.getY() - int(1), ship.getY() + 2):
                    if 1 <= i <= 6 and 1 <= j <= 6 and self.BA[j][i] != 2:
                        self.BA[j][i] = 2
                        self.setShipsAndShadows(1)
            for i in range(ship.getX(), ship.getX() + ship.getSize()):
                self.BA[ship.getY()][i] = 1
                ship.decks[d].append(ship.getY())
                ship.decks[d].append(i)
                d += 1

    def standUpAndShoot(self, shot): # Функция принимает координаты клеточки на поле боя, по которой игрок производит выстрел.
        # Проверяется, производился ли выстрел по этим координатам ранее, и наличие в этой клетке плавсредства. При Повторном
        # выстреле - отказ зачесть попытку, при попадании по цели - безудержная радость. В остальных случаях - просто переход
        # права выстрела к другому игроку.
        y, x = shot
        if self.BA[x][y] < 0:
            return 1
        elif self.BA[x][y] == 1:
            return 2
        else:
            return 0

def myMilitaryPreparations(): #Функция запрашивает у игрока последовательно координаты его боевых судов и их ориентацию, то есть,
    # расположение на поле боя, а не гендерное самоощущение. Содомитам всех видов на войне не место.
    # Проверяет корректность самих введенных данных и возможность размещение корабля на поле боя. При наличии какой-либо
    # ошибки в веденых параметрах добивается от игрока введения правильных значений. Получив-таки приемлимые значения
    # функция провоцирует создание объекта класса Ship и добавляет его в список имеющихся кораблей. Функция возвращает
    # список кораблей.
    fakeBtAq = BattleAquatoria()
    fakeBtAq.setXY([4,4],1)
    ShipsListMy = [Ship(3), Ship(2), Ship(2), Ship(1), Ship(1), Ship(1), Ship(1)] #Список короблей, т.е. элементами списка являются объекты класса Ship, управляемых живым игроком
    addedShips = 0
    while addedShips < len(ShipsListMy):
        myBtAq = BattleAquatoria()
        hopelessnessFlag = False
        for sh in ShipsListMy:
            print('Корабль на ' + str(sh.getSize()) + ' палубы. ')
            addShipNok = 1
            while addShipNok:
                printBA([myBtAq, fakeBtAq])
                InParam = list(input('Введите координату х, координату у, ориентацию: '))
                if len(InParam) != 3:
                    print('Вы ввели ' + str(len(InParam)) + ', а надо ровно 3 величины. Бедте внимательнее!!!')
                    continue
                else:
                    x, y, orientation = list(InParam)
                if sh.setX(x):
                    print('Введено недопустимое значение координаты Х')
                    continue
                elif sh.setY(y):
                    print('Введено недопустимое значение координаты Y')
                    continue
                elif sh.setOr(orientation):
                    print('Введено недопустимое обозначение ориентации корабля')
                    continue
                elif myBtAq.checkShipLocation(sh.getSize(), x, y, orientation) == 1:
                    print('Невозможно такой корабль разместить предложенным способом')
                    continue
                else:
                    myBtAq.addShip(sh)
                    addShipNok = 0
                    addedShips += 1
                    if myBtAq.getShipsAndShadows() >= (myBtAq.sizeBA - 1) ** 2 and addedShips < len(ShipsListMy):
                        print('Невозможно так разместить суда! Начинаем сначала!')
                        hopelessnessFlag = True
                        addedShips = 0
                        for i in range(myBtAq.RsizeBA):
                            for j in range(myBtAq.RsizeBA):
                                myBtAq.BA[i][j] = 0
                        break
                if hopelessnessFlag == True:
                    break
    return [myBtAq, ShipsListMy]

def aiMilitaryPreparations():
    ShipsListAI = [Ship(3), Ship(2), Ship(2), Ship(1), Ship(1), Ship(1), Ship(1)] # Список короблей, т.е. элементами списка являются объекты класса Ship, управляемых программой
    addedShips = 0
    while addedShips < len(ShipsListAI):
        aiBtAq = BattleAquatoria()
        hopelessnessFlag = False
        for sh in ShipsListAI:
            addShipNok = 1
            while addShipNok:
                x = random.randint(1, 1000) % 6 + 1
                y = random.randint(1, 1000) % 6 + 1
                orientation = random.choice(['h', 'v'])
                if aiBtAq.checkShipLocation(sh.getSize(), x, y, orientation) == 1:
                    continue
                else:
                    sh.setX(int(x))
                    sh.setY(int(y))
                    sh.setOr(orientation)
                    aiBtAq.addShip(sh)
                    addShipNok = 0
                    addedShips += 1
                    if aiBtAq.getShipsAndShadows() >= (aiBtAq.sizeBA - 1) ** 2 and addedShips < len(ShipsListAI):
                        hopelessnessFlag = True
                        addedShips = 0
                        for sh in ShipsListAI:
                            sh.decks.clear()
                        for i in range(aiBtAq.RsizeBA):
                            for j in range(aiBtAq.RsizeBA):
                                aiBtAq.BA[i][j] = 0
                        break
            if hopelessnessFlag == True:
                break
    return [aiBtAq, ShipsListAI]

def printBA(BtAqs): # Эта функция печает в косоль поле боя в его текущем состоянии.
    print(' |1|2|3|4|5|6' + ' ' * 10 + ' |1|2|3|4|5|6')
    for i in range(1, BtAqs[0].getSizeBA()):
        prStr0 = str(i)
        prStr1 = str(i)
        for j in range(1, BtAqs[0].getSizeBA()):
            if BtAqs[0].BA[i][j] == 1:
                prStr0 += ('\u25A0')
            elif BtAqs[0].BA[i][j] == int(-1):
                prStr0 +=  'T'
            elif BtAqs[0].BA[i][j] == int(-2):
                prStr0 += 'X'
            else:
                prStr0 += str(BtAqs[0].BA[i][j])     #'O'
        for j in range(1, BtAqs[1].getSizeBA()):
#            if BtAqs[1].BA[i][j] == int(-1):
#                prStr1 += 'T'
#            elif BtAqs[1].BA[i][j] == int(-2):
#                prStr1 += 'X'
#            else:
#                prStr1 += 'O'
            if BtAqs[1].BA[i][j] == 1:
                prStr1 += ('\u25A0')
            elif BtAqs[1].BA[i][j] == int(-1):
                prStr1 +=  'T'
            elif BtAqs[1].BA[i][j] == int(-2):
                prStr1 += 'X'
            else:
                prStr1 += 'O'
        print('|'.join(prStr0) + ' ' * 10 + '|'.join(prStr1))

def letsFighting():
    plCur = 0
    BtAqs = []
    BtShps = []
    print('Наченаем размещать мои корабли')
    myMP = myMilitaryPreparations()
    print('Мои корабли разместили')
    print('Начинаем размещать корабли ИИ')
    aiMP = aiMilitaryPreparations()
    print('Корабли ИИ разместили')
    BtAqs.append(myMP[0])
    BtAqs.append(aiMP[0])
    BtShps.append(myMP[1])
    BtShps.append(aiMP[1])
    myShipsNumber = len(BtShps[0])
    aiShipsNumber = len(BtShps[1])
    Victory = False
    while Victory == False:
        printBA(BtAqs)
        if plCur == 0:
            shot = list(input('Введите координаты, по которым будете стрелять: ').replace(' ',''))
            if len(shot) != 2:
                print('Надо ввести ровно две координаты, а Вы ввели - ' + str(len(shot)))
                continue
            if not all(i.isdigit() for i in shot):
                print('Координаты - это только числа!')
                continue
            if not all(1 <= i <= 6 for i in list(map(int, shot))):
                print('Координаты - это только числа от 1 до 6!')
                continue
            shotResult = BtAqs[1].standUpAndShoot(list(map(int, shot)))
            if shotResult == 1:
                print('Сюда Вы уже стреляли. Будте внимательнее, не расходуйте боеприпасы впустую!')
                continue
            elif shotResult == 2:
                print('Попал!!!')
                for sh in BtShps[1]:
                    for i in range(len(sh.decks)):
                        if int(sh.decks[i][0]) == int(shot[1]) and int(sh.decks[i][1]) == int(shot[0]):
                            sh.setHoles()
                            if sh.getHoles() == sh.getSize():
                                print('Убил!!!')
                                aiShipsNumber -= 1
                                if aiShipsNumber == 0:
                                    print('Это победа!!! Поздравляю!!!')
                                    Victory = True
                BtAqs[1].setXY(shot, int(-2))
            elif shotResult == 0:
                print('Мимо!')
                BtAqs[1].setXY(shot, int(-1))
#                printBA(BtAqs)
                plCur = (plCur + 1) % 2
        elif plCur == 1:
            shot = [random.randint(1,6), random.randint(1,6)]
            print('Бездушная автоматика выстрелила по координатам: ' + str(shot[0]) + str(shot[1]))
            shotResult = BtAqs[0].standUpAndShoot(list(map(int, shot)))
            if shotResult == 1:
                print('Сюда она уже стреляла!!!')
                continue
            elif shotResult == 2:
                print('Попала, сволочь!!!')
                for sh in BtShps[0]:
                    if int(shot[0]) == int(sh.getX()) and int(shot[1]) == int(sh.getY()):
                        sh.setHoles()
                        if sh.getHoles() == sh.getSize():
                            print('Убила!!!')
                            myShipsNumber -= 1
                            if myShipsNumber == 0:
                                print('Вы проиграли!!! Сочувствую!!!')
                                Victory = True
                BtAqs[0].setXY(shot, int(-2))
            elif shotResult == 0:
                print('Мимо!!! Ха-ха-ха!!!')
                BtAqs[0].setXY(shot, int(-1))
#                printBA(BtAqs)
                plCur = (plCur + 1) % 2

letsFighting()
