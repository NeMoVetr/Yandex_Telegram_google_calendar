from gcsa.google_calendar import GoogleCalendar
from gcsa.event import Event
from datetime import datetime, timedelta
from tzlocal import get_localzone

# Импорт функции извлечения сущностей
from extraction_entities import extraction_event_location_data

# Парсинг Яндекс почты
from yandex_parser import fetch_emails

# Парсинг telegram чата
from telegram_parser import fetch_telegram_messages

# Путь учетным данным Google Calendar API
CREDENTIALS_FILE = 'credentials.json'


def parse_datetime(date_str: str, time_str: str):
    """
    Функция преобразования из строки даты и времени в объект datetime с учетом локальной временной зоны.
    """

    local_tz = get_localzone()  # Локальная временная зона
    try:

        event_date = datetime.strptime(date_str, "%d.%m.%Y")  # Преобразование даты
        event_time = datetime.strptime(time_str, "%H:%M").time()  # Преобразование времени
        event_datetime = datetime.combine(event_date, event_time)  # Комбинирование
        return event_datetime.astimezone(local_tz)  # Приведение к локальной временной зоне

    except ValueError as e:
        print(f"Ошибка при преобразовании даты или времени: {e}")
        return


def add_event_from_text(text: str):
    """
    Функция извлечения данных из текста и добавления события в Google Календарь.
    """
    # Извлекаем данные из текста
    extracted_data = extraction_event_location_data(text)

    # Получаем сущности
    event_name = extracted_data.get("EVENT", "Без названия")  # Название события
    location = extracted_data.get("LOCATION", "Без локации")  # Локация события
    date_str = extracted_data.get("DATE")  # Дата события
    time_str = extracted_data.get("TIME")  # Время события

    # Проверяем наличие необходимых данных
    if not date_str or not time_str:
        return

    # Преобразуем дату и время в формат datetime
    start_time = parse_datetime(date_str, time_str)
    if not start_time:
        return

    # Предположим, что событие длится 1 час
    end_time = start_time + timedelta(hours=1)

    # Инициализация Google Календаря
    calendar = GoogleCalendar(credentials_path=CREDENTIALS_FILE)

    # Создание и добавление события
    event = Event(
        summary=event_name,
        start=start_time,
        end=end_time,
        location=location
    )

    calendar.add_event(event)
    print(f"Событие '{event_name}' добавлено в календарь.")


if __name__ == "__main__":
    # Парсинг с почты
    email_data_dict = fetch_emails()

    # Парсинг с чата
    telegram_data_dict = fetch_telegram_messages()

    # Извлечение текста из email_data_dict
    for value in email_data_dict.values():
        text = value.get('Body', '')

        if text:  # Если текст существует
            add_event_from_text(text)

    for value in telegram_data_dict.values():
        text = value.get('Body', '')

        if text:  # Если текст существует
            add_event_from_text(text)
