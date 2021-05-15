try:
    x = int(input('Введите: '))
except ValueError as e:
    print('Вы ввели неправильное число!')
else:
    print(f'Вы ввели правильное число {x}')
finally:
    print('Выход там ->')