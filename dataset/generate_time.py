from itertools import product

# Списки для хранения всех возможных форматов времени, включая часы, минуты, и время суток
hours_full = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
              '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23']
hours_half = ['01', '02', '03', '04', '05', '06', '07', '08', '09', '1', '2', '3', '4', '5', '6', '7', '8', '9', '10',
              '11']

minutes = ['00', '01', '02', '03', '04', '05', '06', '07', '08', '09', '0', '1', '2', '3', '4', '5', '6', '7', '8', '9',
           '10', '11', '12', '13', '14', '15', '16', '17', '18', '19', '20', '21', '22', '23', '24', '25', '26', '27',
           '28', '29', '30', '31', '32', '33', '34', '35', '36', '37', '38', '39', '40', '41', '42', '43', '44', '45',
           '46', '47', '48', '49', '50', '51', '52', '53', '54', '55', '56', '57', '58', '59']

time_of_day = ['a.m.', 'a. m.', 'p.m.', 'p. m.']

hour = ['час', 'часа', 'часов']

midnight = ['24:00', '24:0']
midday = ['12:00', '12:0']

# Текстовые представления часов
hours_words = [
    'один час', 'два часа', 'три часа', 'четыре часа', 'пять часов',
    'шесть часов', 'семь часов', 'восемь часов', 'девять часов',
    'десять часов', 'одиннадцать часов', 'двенадцать часов',
    'тринадцать часов', 'четырнадцать часов', 'пятнадцать часов',
    'шестнадцать часов', 'семнадцать часов', 'восемнадцать часов',
    'девятнадцать часов', 'двадцать часов', 'двадцать один час',
    'двадцать два часа', 'двадцать три часа'
]

# Текстовые представления минут
minutes_words_ten = 'десять'
minutes_words_tens = ['двадцать', 'тридцать', 'сорок', 'пятьдесят', 'шестьдесят']
minutes_words_zero = 'ноль минут'
minute = 'минут'

minutes_words_units = ['одну минуту', 'две минуты', 'три минуты', 'четыре минуты', 'пять минут', 'шесть минут',
                       'семь минут', 'восемь минут', 'девять минут']

minutes_words_intens = ['одиннадцать минут', 'двенадцать минут', 'тринадцать минут', 'четырнадцать минут',
                        'пятнадцать минут', 'шестнадцать минут', 'семнадцать минут', 'восемнадцать минут',
                        'девятнадцать минут']


def time_numbers(f):
    """
    Генерация времени в числовом формате
    """

    for i in product(hours_full, minutes):
        x = ':'.join(i)
        f.write(x + '\n')

    for i in midnight:
        f.write(i + '\n')


def time_numbers_mid(f):
    """
    Генерация времени с указанием времени суток
    """

    for i in product(hours_half, minutes):
        for j in time_of_day:
            x = ':'.join(i)
            x = x + ' ' + j
            f.write(x + '\n')

    for i in midday:
        for j in time_of_day:
            f.write(i + ' ' + j + '\n')


def time_words(f):
    """
    Генерация времени в текстовом формате
    """

    for i in hours_words:
        f.write(i + '\n')

    for i in hours_words:
        f.write(i + ' ' + minutes_words_zero + '\n')

    for i in hours_words:
        f.write(i + ' ' + minutes_words_ten + ' ' + minute + '\n')

    for i in product(hours_words, minutes_words_tens):
        i = ' '.join(i)
        f.write(i + ' ' + minute + '\n')

    for i in product(hours_words, minutes_words_intens):
        i = ' '.join(i)
        f.write(i + '\n')

    for j in hours_words:
        for i in minutes_words_units:
            f.write(j + ' ' + i + '\n')

    for j in hours_words:
        for i in product(minutes_words_tens, minutes_words_units):
            i = ' '.join(i)
            f.write(j + ' ' + i + '\n')


def time_numbers_reduced(f):
    """
    Генерация числового времени, отфильтрованного по определенным минутам
    """

    for i in product(hours_full, minutes):
        x = ':'.join(i)
        y = x.split(':')[-1]
        if y in ['0', '00', '10', '15', '20', '25', '30', '35', '40', '45', '50', '55']:
            f.write(x + '\n')

    for i in midnight:
        f.write(i + '\n')


def create(file: str):
    """
    Функция, которая создает файл с разными форматами времени
    """

    with open(file, 'w', encoding='UTF-8') as f:
        time_numbers(f)
        time_numbers_mid(f)
        time_words(f)
        # time_numbers_reduced(f)


if __name__ == '__main__':
    create('time.txt')
