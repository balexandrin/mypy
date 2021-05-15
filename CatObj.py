from CatClass import Cat

CatsList = []
CatsList.append({'name' : 'Барон', 'sex' : 'Мальчик', 'age' : '2'})
CatsList.append({'name' : 'Сэм', 'sex' : 'Мальчик', 'age' : '2'})

for cattt in CatsList:
    animal = Cat(name = cattt.get("name"), sex = cattt.get("sex"), age = cattt.get("age"))
    print('Имя: ' + animal.getName())
    print('Пол: ' + animal.getSex())
    print('Возраст: ' + animal.getAge())
    print('')