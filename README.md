# Event Extraction and Google Calendar Automation

## Описание

Данный проект предназначен для автоматического извлечения событий из писем Яндекс.Почты и сообщений Telegram, их структурирования с помощью моделей обработки естественного языка (spaCy), и последующего добавления этих событий в Google Календарь.

## Основные возможности

- Сбор сообщений из Яндекс.Почты и Telegram.
- Обработка и разметка текстов для обучения NER-модели.
- Обучение и использование собственной NER-модели spaCy для извлечения сущностей: событие, локация, дата, время.
- Интеграция с Google Calendar API для автоматического создания событий.
- Использование C#-библиотеки Horst для извлечения дат и времени из текста на русском языке.

## Структура проекта

```
.
├── dataset/                # Скрипты и файлы для генерации и хранения датасета
│   ├── generate_database.py
│   ├── database_random.csv
│   ├── events.txt, locations.txt, time.txt, date.txt
├── model/                  # Файлы обученной spaCy-модели
│   ├── config.cfg, meta.json, tokenizer, vocab/, ner/
├── Telegram/               # Сохранённые сообщения Telegram
│   └── telegram_messages.csv
├── Horst/, library_horst_on_C_sharp/ # C#-библиотека для парсинга дат
├── config_telegram.py      # Конфиг для Telegram API
├── extraction_entities.py  # Извлечение сущностей из текста
├── google_calendar.py      # Добавление событий в Google Calendar
├── neural_network_model.py # Обучение NER-модели
├── telegram_parser.py      # Парсер Telegram
├── yandex_parser.py        # Парсер Яндекс.Почты
├── environment.yml         # Описание Python-окружения
└── ...
```

## Установка

1. **Создайте и активируйте окружение:**
   ```bash
   conda env create -f environment.yml
   conda activate Hagging_face
   ```

2. **Установите зависимости для spaCy и Telethon:**
   ```bash
   pip install spacy telethon gcsa
   ```

3. **Настройте доступы:**
   - Для Telegram: заполните `config_telegram.py` своими `api_id` и `api_hash`.
   - Для Google Calendar: получите файл `credentials.json` через Google Cloud Console. 
     Подробная инструкция: [Инструкция API Google Calendar (Habr)](https://habr.com/ru/articles/525680/)

4. **Сгенерируйте датасет (опционально):**
   ```bash
   python dataset/generate_database.py
   ```

5. **Обучите модель (опционально):**
   ```bash
   python neural_network_model.py
   ```

## Использование

1. **Запуск основного сценария:**
   ```bash
   python google_calendar.py
   ```
   Скрипт автоматически соберёт новые письма и сообщения, извлечёт события и добавит их в Google Календарь.

2. **Парсинг только e-mail или Telegram:**
   - `python yandex_parser.py`
   - `python telegram_parser.py`

## Документация по модулям

### yandex_parser.py
- Получает новые письма с Яндекс.Почты через IMAP.
- Очищает текст писем, фильтрует массовые рассылки.
- Возвращает словарь с отправителем, темой, телом и датой письма.

### telegram_parser.py
- Получает сообщения из всех чатов Telegram.
- Сохраняет новые сообщения в CSV.
- Возвращает словарь с текстом и датой сообщений.

### extraction_entities.py
- Использует spaCy-модель для извлечения сущностей EVENT, LOCATION.
- Для извлечения даты и времени использует C#-библиотеку Horst через pythonnet.
- Функция `extraction_event_location_data(text)` возвращает словарь с найденными сущностями.

### neural_network_model.py
- Обучает NER-модель spaCy на кастомном датасете.
- Сохраняет модель в папку `model/`.

### google_calendar.py
- Извлекает события из текстов (e-mail, Telegram).
- Добавляет события в Google Календарь через API.

### dataset/generate_database.py
- Генерирует синтетический датасет для обучения NER-модели.
- Использует списки событий, локаций, дат и времени.

### Библиотека Horst (C#)
- Для извлечения дат и времени из текстов на русском языке используется библиотека Horst, реализованная на C#.
- Интеграция осуществляется через pythonnet (clr).
- Подробнее о библиотеке: [Библиотека Horst (Habr)](https://habr.com/ru/articles/471204/)
- Исходники и сборки находятся в папках `Horst/` и `library_horst_on_C_sharp/`.

## Форматы данных

- **dataset/database_random.csv**: обучающая выборка для NER-модели.
- **Telegram/telegram_messages.csv**: сообщения Telegram (текст, дата).
- **model/**: файлы обученной spaCy-модели.

## Требования

- Python 3.10+
- Conda
- Доступ к Google Calendar API
- Доступ к Telegram API

