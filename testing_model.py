from transformers import BertForTokenClassification, BertTokenizerFast

checkpoint_path = 'results/checkpoint-1500'

# Загрузка модели и токенизатора
model = BertForTokenClassification.from_pretrained(checkpoint_path)
tokenizer = BertTokenizerFast.from_pretrained(checkpoint_path)

# Текст для предсказания
text = "I want to buy a new Hamar Plant Stand - Ash"

# Токенизация
inputs = tokenizer(text, return_tensors="pt", truncation=True, is_split_into_words=False)

# Получение предсказаний
outputs = model(**inputs)

# Индексы предсказанных меток
predictions = outputs.logits.argmax(dim=-1)

# Список меток, использованных для обучения
label_list = ["O", "B-Product", "I-Product"]

# Декодирование предсказаний
predicted_labels = [label_list[pred] for pred in predictions[0].numpy().tolist()]

# Вывод токенов и их меток
tokens = tokenizer.convert_ids_to_tokens(inputs["input_ids"][0])
for token, label in zip(tokens, predicted_labels):
    print(f"{token}: {label}")
