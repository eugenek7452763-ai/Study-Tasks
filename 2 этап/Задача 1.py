#  Счетчик символов
#  Ввод исходных данных, объявление переменных
st = "Today is good day!: Сегодня хороший день!"
letters = 0
digits = 0
spaces = 0
for i in st: # Цикл проверок на буквы, цифры и пробелы
    if ('a' <= i <= 'z') or ('A' <= i <= 'Z'):
        letters += 1

    elif ('а' <= i <= 'я') or ('А' <= i <= 'Я'):
        letters += 1

    elif '0' <= i <= '9':
        digits += 1

    elif i == ' ':
        spaces += 1
#  Вывод символов
print(f'Буквы:{letters}, Цифры:{digits}, Пробелы:{spaces}')