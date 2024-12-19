import csv
import os
import asyncio
from datetime import datetime, timedelta, timezone
from telethon import TelegramClient

from config_telegram import api_id, api_hash

client = TelegramClient('test_tg', api_id, api_hash)

# Имя выходного CSV файла
output_file = 'Telegram/telegram_messages.csv'


async def parser():
    """
    Функция для парсинга сообщений Telegram
    """

    dialogs = await client.get_dialogs()

    # Проверка, существует ли CSV файл
    if os.path.exists(output_file):
        # Если файл существует, считываем дату последнего сообщения
        last_date = get_last_date_from_csv(output_file)
    else:
        # Если файл не существует, создаем его и записываем заголовок
        with open(output_file, 'w', newline='', encoding='utf-8') as csvfile:
            writer = csv.writer(csvfile)
            writer.writerow(['Message', 'Date'])  # Заголовки столбцов
        last_date = datetime.now(timezone.utc) - timedelta(days=4)  # Устанавливаем дату 4 дня назад

    messages_dict = {}

    for dialog in dialogs:
        if dialog.title != 'Telegram':
            messages = client.iter_messages(dialog)
            async for message in messages:
                if message.date > last_date:  # Проверка на дату
                    if message.text:  # Проверка на наличие текста

                        # Добавляем в словарь
                        messages_dict[message.id] = {
                            'Body': message.text,
                            'date': message.date
                        }

                        # Сохраняем сообщение и дату в CSV файл
                        with open(output_file, 'a', newline='', encoding='utf-8') as csvfile:
                            writer = csv.writer(csvfile)
                            writer.writerow([message.text, message.date])  # Записываем сообщение и дату

                        await asyncio.sleep(1)  # Задержка в 1 секунду

    return messages_dict


def get_last_date_from_csv(file_path):
    """
    Получение самой актуальной даты из csv-файла
    """

    last_date = None
    with open(file_path, 'r', encoding='utf-8') as csvfile:
        reader = csv.reader(csvfile)
        next(reader)
        for row in reader:
            message_date = datetime.fromisoformat(row[1])  # Преобразуем строку в дату
            if last_date is None or message_date > last_date:
                last_date = message_date  # Обновляем последнюю дату
    return last_date if last_date else datetime.now(timezone.utc) - timedelta(
        days=4)  # Возвращаем 4 дня назад, если нет сообщений


def fetch_telegram_messages():
    """
    Обёртка для вызова TelegramClient
    """

    with client:
        # Запуск в режиме "пока есть хоть одна работающая функция внутри":
        return client.loop.run_until_complete(parser())
