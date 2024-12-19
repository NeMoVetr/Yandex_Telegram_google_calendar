import clr
import spacy

clr.AddReference("Horst/library_horst")  # Добавление ссылки на библиотеку Horst

from HorstLibrary import HorsWrapper
import re


def extraction_time(text: str) -> str:
    """
    Функция извлекает время из текста и преобразует его в формат HH:MM.
    """

    # Словарь для преобразования текстовых чисел в числовые значения
    hours_mapping = {
        "один": 1, "два": 2, "три": 3, "четыре": 4, "пять": 5,
        "шесть": 6, "семь": 7, "восемь": 8, "девять": 9,
        "десять": 10, "одиннадцать": 11, "двенадцать": 12
    }
    # Список регулярных выражений для поиска времени в тексте
    time_patterns = [
        r"в (\d{1,2}) час(?:а|ов)?(?: (утра|дня|вечера|ночи))?",  # Формат с числовым значением часа
        r"в (\w+) час(?:а|ов)?(?: (утра|дня|вечера|ночи))?"  # Формат с текстовым значением часа
    ]

    matches = []
    # Поиск всех совпадений в тексте для каждого паттерна
    for pattern in time_patterns:
        matches += re.findall(pattern, text.lower())

    if not matches:
        return None  # Если время не найдено, вернуть None

    for match in matches:
        hour, period = match  # Разделение на час и период времени

        # Проверка и преобразование числового или текстового значения часа
        if hour.isdigit():
            hour = int(hour)
        elif hour in hours_mapping:
            hour = hours_mapping[hour]
        else:
            continue  # Если значение часа некорректное, пропустить

        # Корректировка времени в зависимости от указанного периода
        if period == "утра" and hour == 12:
            hour = 0
        elif period == "дня" and hour < 12:
            hour += 12
        elif period == "вечера" and hour < 12:
            hour += 12
        elif period == "ночи" and hour < 12:
            hour += 12 if hour != 12 else 0

        # Возврат времени в формате HH:MM
        return f"{hour:02d}:00"

    return None  # Если совпадения обработать не удалось, вернуть None


def extraction_event_location_data(text: str) -> dict:
    """
    Функция извлекает события, места, даты и время из текста.
    """

    nlp = spacy.load("model")  # Загрузка предобученной модели spaCy
    doc = nlp(text)  # Обработка текста через NLP-модель

    entities = {}  # Словарь для хранения извлечённых сущностей

    # Извлечение сущностей типа "Событие" и "Локация"
    for ent in doc.ents:
        if ent.label_ in ["EVENT", "LOCATION"]:
            entities[f"{ent.label_}"] = ent.text

    # Если не удалось извлечь дату, возвращаем пустой словарь
    try:
        # Извлечения сущностей типа "Дата"
        wrapper = HorsWrapper().ParseDateTime(text).split()
    except Exception:
        return {}

    # Если не удалось извлечь дату или нет сущностей
    if not entities:
        return {}

    wrapper = wrapper

    entities["DATE"] = wrapper[0]

    # Извлечения сущностей типа "Время"
    for token in text.split():
        if ":" in token:  # Если токен содержит символ ":", предполагаем, что это время
            entities["TIME"] = token
        elif extraction_time(text) and "TIME" not in entities:  # Если время ещё не добавлено
            entities["TIME"] = extraction_time(text)

    return entities
