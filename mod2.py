import mod1

r = float(input('Введите радиус: '))
a = float(input('Введите сторону квадрата'))
if mod1.Cl(r) > mod1.Sq(a):
    print('Круг больше')
elif mod1.Cl(r) < mod1.Sq(a):
    print('Квадрат больше')
else:
    print('Поровну')