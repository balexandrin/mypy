import requests  # импортируем наш знакомый модуль
import lxml.html
from lxml import etree

#/html/body/div/div[3]/div/section/div[2]/div[1]/div/ul/li[1]/a
#/html/body/div/div[3]/div/section/div[2]/div[1]/div/ul/li[1]

# создадим объект ElementTree. Он возвращается функцией parse()
tree = etree.parse('Welcome to Python.org.html', lxml.html.HTMLParser())
# попытаемся спарсить наш файл с помощью html парсера. Сам html - это то что мы скачали и поместили в папку из браузера.

ul = tree.findall(
    'body/div/div[3]/div/section/div[3]/div[1]/div/ul/li')  # помещаем в аргумент методу findall скопированный xpath. Здесь мы получим все элементы списка новостей. (Все заголовки и их даты)

# создаём цикл в котором мы будем выводить название каждого элемента из списка
for li in ul:
    a = li.find(
        'a')  # в каждом элементе находим где хранится заголовок новости. У нас это тег <a>. Т.е. гиперссылка на которую нужно нажать, чтобы перейти на страницу с новостью. (Гиперссылки в html это всегда тэг <a>)
    print(a.text)  # из этого тега забираем текст - это и будет нашим названием
