import matplotlib.pyplot as plt
import pandas as pd
import ast
import spacy
from spacy.training import Example


def learning_model():
    """
    Функция для обучения модели spaCy.
    """

    # Обучение производим GPU для ускорения работы spaCy
    spacy.require_gpu()

    # Загружаем данные из CSV файла
    df = pd.read_csv("dataset/database_random.csv", encoding='utf-8', dtype=str)
    print("Download successfully")  # Сообщение об успешной загрузке

    # Создаем пустую языковую модель для русского языка
    nlp = spacy.blank("ru")

    # Проверяем, есть ли в модели конвейер NER (распознавание именованных сущностей)
    if "ner" not in nlp.pipe_names:
        nlp.add_pipe("ner", last=True)  # Добавляем компонент NER в конвейер

    # Получаем ссылку на компонент NER
    ner = nlp.get_pipe("ner")

    # Определяем метки для именованных сущностей
    labels = ["EVENT", "LOCATION"]  # Метки: событие и местоположение

    # Добавляем метки в компонент NER
    for label in labels:
        ner.add_label(label)

    # Инициализируем список для хранения обучающих данных
    TRAIN_DATA = []

    # Проходим по каждой строке в DataFrame
    for i, row in df.iterrows():
        # Извлекаем текст предложения и убираем лишние символы
        text = row['sentence'].strip().replace("'", "")

        # Создаем объект документа из текста
        doc = nlp.make_doc(text)

        # Извлекаем аннотации сущностей из строки
        entities = ast.literal_eval(row['definition'])

        # Добавляем данные в обучающий набор
        TRAIN_DATA.append((text, {"entities": entities}))

    # Инициализируем оптимизатор для обучения модели
    optimizer = nlp.begin_training()

    # Задаем количество эпох обучения
    epochs = 10
    losses_history = []  # Список для хранения истории потерь

    # Основной цикл обучения
    for epoch in range(epochs):
        print(f"Start the learning")

        losses = {}  # Словарь для хранения потерь за эпоху

        # Обновляем модель на каждом примере из обучающего набора
        for text, annotation in TRAIN_DATA:
            example = Example.from_dict(nlp.make_doc(text), annotation)  # Создаем пример
            nlp.update([example], drop=0.2, sgd=optimizer, losses=losses)  # Обновляем модель

        # Сохраняем потери и выводим их
        losses_history.append(losses['ner'])
        print(f"Epoch {epoch + 1}: Losses {losses['ner']}")

        # Построение графика зависимости потерь от эпох
        plot_loss_history(epochs, losses_history)

        # Сохраняем обученную модель на диск
        nlp.to_disk("model")
        print("Model saved")  # Сообщение об успешном сохранении модели


def plot_loss_history(epochs, losses_history):
    """
    Построение графика зависимости потерь от эпох
    """

    plt.figure(figsize=(8, 6))
    plt.plot(range(epochs), losses_history, label="Потери (NER)")
    plt.xlabel("Эпоха")
    plt.ylabel("Потери")
    plt.title("График зависимости потерь")
    plt.grid()
    plt.show()

