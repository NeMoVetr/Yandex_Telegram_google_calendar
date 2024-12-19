import imaplib
import email
from datetime import datetime, timedelta
import pytz
import re

# Настройки для подключения к Яндекс.Почте
EMAIL = ''  # Email
PASSWORD = ''  # Пароль SMTP уникальный ключ


def clean_email_body(body: str):
    """
    Функция для очистки сообщения от ссылок и лишних пробелов
    """

    body = re.sub(r'http\S+|www\S+|https\S+', '', body, flags=re.MULTILINE)
    body = re.sub(r'\s+', ' ', body).strip()
    return body


#
def get_email_body(msg: email.message.EmailMessage):
    """
    Функция для редактирования тестовой части сообщения убирает лишнее в сообщениях
    """

    if msg.is_multipart():
        for part in msg.walk():
            if part.get_content_type() == 'text/plain':
                return clean_email_body(part.get_payload(decode=True).decode(part.get_content_charset()))
            elif part.get_content_type() == 'text/html':
                return None  # Если это HTML, возвращаем None
    else:
        if msg.get_content_type() == 'text/plain':
            return clean_email_body(msg.get_payload(decode=True).decode(msg.get_content_charset()))
        elif msg.get_content_type() == 'text/html':
            return None  # Если это HTML, возвращаем None
    return None  # Если ничего не найдено


def is_individual_email(from_: str):
    """Функция проверки, является ли письмо от отдельного пользователя."""

    mass_senders = ['promo', 'newsletter', 'offers', 'discounts', 'info', 'support']
    return not any(sender in from_.lower() for sender in mass_senders)


def fetch_emails() -> dict:
    """
    Функция для получения новых писем с Яндекс.Почты
    """

    # Устанавливаем дату на 7 дней назад для поиска новых писем
    date_limit = datetime.now(pytz.timezone('Europe/Moscow')) - timedelta(days=7)

    # Подключение к Яндекс.Почте
    mail = imaplib.IMAP4_SSL('imap.yandex.ru')
    mail.login(EMAIL, PASSWORD)

    # Выбор папки "Входящие"
    mail.select('inbox')

    # Поиск писем с установленной датой со статусом "Новое"
    status, messages = mail.search(None, f'SINCE {date_limit.strftime("%d-%b-%Y")} UNSEEN')

    # Словарь для хранения данных
    email_data_dict = {}

    # Обработка найденных писем
    for num in messages[0].split():
        # Получение письма
        status, msg_data = mail.fetch(num, '(RFC822)')
        msg = email.message_from_bytes(msg_data[0][1])

        # Извлечение информации
        from_ = msg['from']  # Адрес отправителя
        subject = msg['subject']  # Тема сообщения
        body = get_email_body(msg)  # Получаем тело сообщения
        date_ = msg['date']  # Дата отправления сообщения
        date_parsed = email.utils.parsedate_to_datetime(date_)  # Парсим дату из заголовка

        # Устанавливаем временную зону для date_parsed
        date_parsed = date_parsed.replace(tzinfo=pytz.timezone('Europe/Moscow'))

        # Проверяем, если дата письма больше или равна дате лимита
        if date_parsed >= date_limit and is_individual_email(from_) and body is not None:
            # Добавление данных в список
            email_data_dict[num] = {
                'Sender': from_,  # Сохраняем адрес отправителя
                'Subject': subject,  # Сохраняем тему сообщения
                'Body': body,  # Сохраняем тело сообщения
                'Date': date_  # Сохраняем дату отправления
            }

            # Помечаем письмо как прочитанное
            mail.store(num, '+FLAGS', '\\SEEN')

    # Закрытие соединения
    mail.logout()

    return email_data_dict
