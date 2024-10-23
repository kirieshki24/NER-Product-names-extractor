import csv

with open('data/parsed_text.txt', 'r', encoding='utf-8') as file:
    list1 = file.read().split('\n')
with open('data/data_100.txt', 'r', encoding='utf-8') as file:
    list2 = file.read().split('\n')

# Функция для BIO-разметки на основе сопоставления строк из двух списков
def create_bio_tags_from_lists(list1, list2):
    bio_data = []

    # Проходим по каждому продукту из первого списка
    for product in list1:
        tokens = product.split()  # Разбиваем строку на токены
        bio_tags = ["O"] * len(tokens)  # Изначально все токены помечаем как O

        # Проверяем наличие токенов продукта в строках из второго списка
        for line in list2:
            if line.lower() in product.lower():  # Поиск соответствий
                product_tokens = line.split()
                start_index = -1

                # Поиск индекса начала соответствия в строке
                for i in range(len(tokens)):
                    if tokens[i:i+len(product_tokens)] == product_tokens:
                        start_index = i
                        break

                # Проставляем BIO метки
                if start_index != -1:
                    bio_tags[start_index] = "B-PRODUCT"
                    for j in range(1, len(product_tokens)):
                        bio_tags[start_index + j] = "I-PRODUCT"
        
        # Добавляем размеченные токены в общий список, объединяя метки в строку
        bio_data.append((product, " ".join(bio_tags)))

    return bio_data

output_file = 'data/bio_tagged_dataset.csv'

bio_data = create_bio_tags_from_lists(list1, list2)

with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)
    writer.writerow(["Sentence", "BIO Tags"]) 

    for sentence, tags in bio_data:
        writer.writerow([sentence, tags])

print(f"BIO-разметка сохранена в файл: {output_file}")