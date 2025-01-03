# Формирование списка годов с сокращённым форматом (двухзначные числа, от 20 до 30)
year_2 = []
for i in range(20, 31):
    year_2.append(str(i))

# Формирование списка годов с полным форматом (четырёхзначные числа, от 2020 до 2030)
year_4 = []
for i in range(2020, 2031):
    year_4.append(str(i))

# Словарь с месяцами в различных форматах:
# 0 - названия месяцев с заглавной буквы
# 1 - названия месяцев с маленькой буквы
# 2 - месяцы в числовом формате без ведущего нуля
# 3 - месяцы в числовом формате с ведущим нулём
months = {
    0: ["Января", "Февраля", "Марта", "Апреля", "Мая", "Июня", "Июля", "Августа", "Сентября", "Октября", "Ноября",
        "Декабря"],
    1: ["января", "февраля", "марта", "апреля", "мая", "июня", "июля", "августа", "сентября", "октября", "ноября",
        "декабря"],
    2: ['1', '2', '3', '4', '5', '6', '7', '8', '9', '10', '11', '12'],
    3: ['01', '02', '03', '04', '05', '06', '07', '08', '09', '10', '11', '12']
}

# Словарь с информацией о месяцах:
# 'feb' - индекс февраля
# 'big_months' - индексы месяцев с 31 днём
# 'small_months' - индексы месяцев с 30 днями
months_size = {
    'feb': 1,
    'big_months': [0, 2, 4, 6, 7, 9, 11],
    'small_months': [3, 5, 8, 10]
}

# Словарь с датами для месяцев разной продолжительности:
# 'dates_feb' - даты февраля, включая 29 для високосного года
# 'dates_small' - даты для месяцев с 30 днями
# 'dates_big' - даты для месяцев с 31 днём
months_dates = {
    'dates_feb': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                  '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26',
                  '27', '28', '29'],
    'dates_small': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                    '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25',
                    '26', '27', '28', '29', '30'],
    'dates_big': ['01', '02', '03', '04', '05', '06', '07', '08', '09', '1', '2', '3', '4', '5', '6', '7', '8', '9',
                  '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26',
                  '27', '28', '29', '30', '31']
}


def date_words(f):
    """
    Генерация дат в текстовом формате
    """
    for letter in range(2):  # Перебираем форматы месяцев: 0 и 1 (заглавная/строчная буква)
        i = 0  # Индекс месяца
        for month in months[letter]:  # Перебираем все месяцы в текущем формате

            # Определяем набор дней в зависимости от месяца
            if i == months_size['feb']:
                dates = months_dates['dates_feb']
            elif i in months_size['small_months']:
                dates = months_dates['dates_small']
            elif i in months_size['big_months']:
                dates = months_dates['dates_big']

            # Формируем строки вида "1 января" и записываем их в файл
            for date in dates:
                x = date + ' ' + month
                f.write(x + '\n')

            i += 1  # Увеличиваем индекс месяца


def date_words_2(f):
    """
    Генерация дат в текстовом формате с сокращённым годом (например, "1 января 24 года")
    """
    for letter in range(2):  # # Перебираем форматы месяцев
        i = 0  # Индекс месяца
        for month in months[letter]:  # Перебираем все месяцы в текущем формате

            if i == months_size['feb']:
                dates = months_dates['dates_feb']
            elif i in months_size['small_months']:
                dates = months_dates['dates_small']
            elif i in months_size['big_months']:
                dates = months_dates['dates_big']

            for u in [' года', ' г.']:  # Форматы окончания года
                for year in year_2:  # Перебор двухзначных годов
                    for date in dates:
                        x = date + ' ' + month + ' ' + year + u
                        f.write(x + '\n')

            i += 1  # Увеличиваем индекс месяца


def date_words_4(f):
    """
    Генерация строк в формате "дата месяц год" для полных (четырехзначных) годов
    """
    for letter in range(2):  # Перебираем заглавные и строчные месяцы (индексы 0 и 1 в словаре months)
        i = 0  # Индекс месяца
        for month in months[letter]:  # Перебираем все месяцы в текущем формате

            if i == months_size['feb']:
                dates = months_dates['dates_feb']
            elif i in months_size['small_months']:
                dates = months_dates['dates_small']
            elif i in months_size['big_months']:
                dates = months_dates['dates_big']

            # Определяем, какие даты использовать в зависимости от размера месяца
            for u in [' года', ' г.']:
                for year in year_4:  # Перебираем все четырехзначные годы
                    for date in dates:  # Перебираем все даты месяца
                        x = date + ' ' + month + ' ' + year + u
                        f.write(x + '\n')  # Записываем строку в файл

            i += 1  # Увеличиваем индекс месяца


def date_number_2(f):
    """
    Генерация строк в формате "дд.мм.гг" для двухзначных годов
    """

    for letter in range(3, 4):  # Используем числовое представление месяцев (индекс 3 в словаре months)
        i = 0  # Индекс месяца
        for month in months[letter]:  # Перебираем все месяцы в числовом формате

            # Определяем, какие даты использовать в зависимости от размера месяца
            if i == months_size['feb']:
                dates = months_dates['dates_feb']
            elif i in months_size['small_months']:
                dates = months_dates['dates_small']
            elif i in months_size['big_months']:
                dates = months_dates['dates_big']

            # Генерируем строки в формате "дд.мм.гг"
            for year in year_2:  # Перебираем все двухзначные годы
                for date in dates:  # Перебираем все даты месяца
                    x = date + '.' + month + '.' + year
                    f.write(x + '\n')  # Записываем строку в файл

            i += 1  # Увеличиваем индекс месяца


def date_number_4(f):
    """
    Генерация строк в формате "дд.мм.гггг" для четырехзначных годов
    """
    for letter in range(3, 4):  # Используем числовое представление месяцев (индекс 3 в словаре months)
        i = 0  # Индекс месяца
        for month in months[letter]:  # Перебираем все месяцы в числовом формате

            # Определяем, какие даты использовать в зависимости от размера месяца
            if i == months_size['feb']:
                dates = months_dates['dates_feb']
            elif i in months_size['small_months']:
                dates = months_dates['dates_small']
            elif i in months_size['big_months']:
                dates = months_dates['dates_big']

            # Генерируем строки в формате "дд.мм.гггг"
            for year in year_4:  # Перебираем все четырехзначные годы
                for date in dates:  # Перебираем все даты месяца
                    x = date + '.' + month + '.' + year
                    f.write(x + '\n')  # Записываем строку в файл

            i += 1  # Увеличиваем индекс месяца


def date_number_2024(f):
    """
    Генерация строк в формате "дд.мм.24" для конкретного года (2024)
    """
    for letter in range(3, 4):  # Используем числовое представление месяцев (индекс 3 в словаре months)
        i = 0
        for month in months[letter]:  # Перебираем все месяцы в числовом формате

            # Определяем, какие даты использовать в зависимости от размера месяца
            if i == months_size['feb']:
                dates = months_dates['dates_feb']
            elif i in months_size['small_months']:
                dates = months_dates['dates_small']
            elif i in months_size['big_months']:
                dates = months_dates['dates_big']

            # Генерируем строки в формате "дд.мм.24"
            for date in dates:  # Перебираем все даты месяца
                x = date + '.' + month + '.24'
                f.write(x + '\n')  # Записываем строку в файл

            i += 1  # Увеличиваем индекс месяца


def create(file: str):
    """
    Создание файла и вызов всех функций генерации дат
    """
    with open(file, 'w', encoding='UTF-8') as f:
        date_words(f)  # Генерация дат в формате "дата месяц"
        date_words_2(f)  # Генерация дат в формате "дата месяц год (двухзначный)"
        date_words_4(f)  # Генерация дат в формате "дата месяц год (четырехзначный)"
        date_number_2(f)  # Генерация дат в формате "дд.мм.гг"
        date_number_4(f)  # Генерация дат в формате "дд.мм.гггг"
        date_number_2024(f)  # Генерация дат в формате "дд.мм.24"


if __name__ == '__main__':
    create('date.txt')
