import csv
from random import choice
from random import randint
from itertools import permutations


def events():
    """
    Открывает файл с событиями
    """

    with open('dataset/events.txt', 'r', encoding='UTF-8') as f:
        array = []
        for i in f:
            array.append(i[:-1])
        return array


def locations():
    """
    Открывает файл с локациями
    """

    with open('dataset/locations.txt', 'r', encoding='UTF-8') as f:
        array = []
        for i in f:
            array.append(i[:-1])
        return array


def times():
    """
    Открывает файл со временем
    """

    with open('dataset/time.txt', 'r', encoding='UTF-8') as f:
        array = ['полдень', 'Полдень', 'полночь', 'Полночь']
        for i in f:
            array.append(i[:-1])
        return array


def dates():
    """
    Открывает файл с датами
    """

    with open('dataset/date.txt', 'r', encoding='UTF-8') as f:
        array = ['Сегодня', 'сегодня', 'Завтра', 'завтра', 'Послезавтра', 'послезавтра']
        for i in f:
            array.append(i[:-1])
        return array


pretext = ['В', 'в']

verb_event = ['Будет', 'будет', 'Запланирован', 'запланирован', 'Запланировано', 'запланировано', 'Запланирована',
              'запланирована']

verb_location = ['Собираемся', 'собираемся']

appeals = ['Коллеги,', 'коллеги,', 'Уважаемые коллеги,', 'уважаемые коллеги,', 'Друзья,', 'друзья,', 'Товарищи,',
           'товарищи,', 'Работники,', 'работники,', 'Работники компании,', 'работники компании,']


def create_definition(sentence, event=None, location=None, date=None, time=None):
    """
    Создает разметку для предложения

    Аргументы:
        sentence (string): предложение, для которого создается разметка
        event (string, optional): событие в предложении. По умолчанию None.
        location (string, optional): локация в предложении. По умолчанию None.
        date (string, optional): дата в предложении. По умолчанию None.
        time (string, optional): время в предложении. По умолчанию None.
    """

    EVENT = []
    LOCATION = []
    DATE = []
    TIME = []

    substrings = []
    indexes = []

    if event != None:
        substrings.append(event)
        indexes.append(EVENT)

    if location != None:
        substrings.append(location)
        indexes.append(LOCATION)

    if date != None:
        substrings.append(date)
        indexes.append(DATE)

    if time != None:
        substrings.append(time)
        indexes.append(TIME)

    # Нахождение частей предложения
    i = 0
    while i < (len(substrings)):
        # Поиск индекса подстроки в предложении
        index = sentence.find(substrings[i])

        if index == -1:
            substrings.pop(i)
            indexes.pop(i)
            continue

        indexes[i].append(index)
        index += len(substrings[i])
        indexes[i].append(index)

        i += 1

    indexes.sort()

    definition = "["

    # Добавление информации о нахождении подстрок
    for numbers in indexes:
        position = ""

        if numbers[0] == sentence.find(event):
            position = f"({numbers[0]}, {numbers[1]}, 'EVENT')"

        if numbers[0] == sentence.find(location):
            position = f"({numbers[0]}, {numbers[1]}, 'LOCATION')"

        if numbers[0] == sentence.find(date):
            position = f"({numbers[0]}, {numbers[1]}, 'DATE')"

        if numbers[0] == sentence.find(time):
            position = f"({numbers[0]}, {numbers[1]}, 'TIME')"

        definition += position

    definition = definition.replace(')(', '), (')
    definition += "]"

    return definition


def create_sentences(event=None, location=None, date=None, time=None):
    """
    Создание предложений на основе частей

    Аргументы:
        event (string, optional): событие. По умолчанию None.
        location (string, optional): локация. По умолчанию None.
        date (string, optional): дата. По умолчанию None.
        time (string, optional): время. По умолчанию None.
    """

    date_part = date

    # Генерация частей предложения с временем
    time_part = []
    for i in pretext:
        time_part.append(f"{i} {time}")

    # Генерация частей предложения с событиями
    event_part = []
    for i in verb_event:
        event_part.append(f"{i} {event}")
        event_part.append(f"У нас {i} {event}")
        event_part.append(f"у нас {i} {event}")
        event_part.append(f"У нас {event}")
        event_part.append(f"у нас {event}")

    # Генерация частей предложения с локациями
    location_part = []
    for i in pretext:
        location_part.append(f"{i} {location}")

    for i in verb_location:
        location_part.append(f"{i} {pretext[1]} {location}")

    sentences = []

    # Создание всех вариантов предложений
    for time_part_element in time_part:
        for event_part_element in event_part:
            for location_part_element in location_part:
                for words in range(2, 4):
                    # Создание перестановок частей предложения
                    for i in permutations([date_part, time_part_element, event_part_element, location_part_element],
                                          r=words):
                        sentence = ' '.join(i)
                        sentences.append(sentence)

                        # Добавление обращений к предложениям
                        for appeal in appeals:
                            sentences.append(f"{appeal} {sentence}")

    return sentences


def create_random(count):
    """
    Создание файла с предложениями
    """

    with open('database_random.csv', 'w', newline='', encoding='UTF-8') as csvfile:
        fieldnames = ['sentence', 'definition']
        writer = csv.DictWriter(csvfile, fieldnames=fieldnames)
        writer.writeheader()

        # Создание предложений и их определений
        for _ in range(count):
            # Выбор случайных частей предложения
            event = choice(events())
            location = choice(locations())
            date = choice(dates())
            time = choice(times())

            sentences = create_sentences(event, location, date, time)

            # Выбор случайного предложения из списка
            sentence = sentences[randint(0, len(sentences) - 1)]

            definition = create_definition(sentence, event, location, date, time)

            writer.writerow({
                'sentence': sentence,
                'definition': definition
            })


def main():
    """
    Функция генерации dateset
    """

    print("Начало работы")
    create_random(10000)
    print("Работа завершена")


if __name__ == "__main__":
    main()
