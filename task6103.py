class Customer:
    def __init__(self, name, surname, balance = int(0)):
        self.name = name
        self.surname = surname
        if isinstance(balance, int) and balance >= 0:
            self.balance = balance
        else: print('Таких денег на балансе быть не может!')

    def coming(self, sum):
        if sum.isdigit() and int(sum) >= 0:
            self.balance += int(sum)
        else:print('Добавить такую сумму невозможно!')

    def expense(self, sum):
        if sum.isdigit() and sum >= 0:
            if self.balance >= sum:
                self.balance -= sum
            else:
                print('Недостаточно средств для списания! \nОперация невозможна!')
        else:print('Списать такую сумму невозможно!')

    def get_balance(self):
        return self.balance

    def get_name(self):
        return self.name + ' ' + self.surname

    def print_balance(self):
        print('Клиент: ' + self.name + ' ' + self.surname + '. Баланс = ' + str(self.balance))

buyer1 = Customer('Иван', 'Петров')
buyer2 = Customer('Петр', 'Иванов', 500)

mans =[buyer1, buyer2]
for man in mans:
    if man.get_balance() == 0:
        x = input('Добавте денег покупателю по имени ' + man.get_name() + '\n')
        man.coming(x)
    man.print_balance()
