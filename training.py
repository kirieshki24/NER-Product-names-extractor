import csv
import pandas as pd
from datasets import Dataset
from transformers import AutoTokenizer, AutoModelForTokenClassification, TrainingArguments, Trainer
import transformers

def csv_opener(csv_file):
    data_list = []

    # Открываем файл и читаем его содержимое
    with open(csv_file, mode='r', newline='', encoding='utf-8') as file:
        # Создаем объект reader для чтения CSV
        csv_reader = csv.reader(file)

        # Пропускаем заголовок (если он есть)
        header = next(csv_reader)

        # Читаем данные построчно и добавляем их в список
        for row in csv_reader:
            data_list.append(row)
    return data_list

arr = csv_opener('data/bio_tagged_dataset.csv')
data = []
for i in arr:
    data.append({"tokens": list(i[0].split()), "ner_tags": list(i[1].split())})

# Создание DataFrame
df = pd.DataFrame(data)

# Преобразование в Dataset
dataset = Dataset.from_pandas(df)

label_list = ["O", "B-PRODUCT", "I-PRODUCT"]

# Загрузка токенизатора и модели
model_name = "bert-base-cased"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = AutoModelForTokenClassification.from_pretrained(model_name, num_labels=len(label_list))

print('Tokenizing...')

def tokenize_and_align_labels(examples):
    tokenized_inputs = tokenizer(examples["tokens"], truncation=True, padding='max_length', is_split_into_words=True)
    labels = []
    for i, label in enumerate(examples["ner_tags"]):
        word_ids = tokenized_inputs.word_ids(batch_index=i)  # Получение индексов слов
        label_ids = []
        previous_word_idx = None
        for word_idx in word_ids:
            if word_idx is None:
                label_ids.append(-100)  # Игнорируем токены, которые не являются частью слова
            elif word_idx != previous_word_idx:
                # Преобразуем метку в индекс из списка label_list
                label_ids.append(label_list.index(label[word_idx]))
            else:
                label_ids.append(-100)  # Игнорируем субтокены
            previous_word_idx = word_idx
        labels.append(label_ids)
    # Добавление меток в токенизированный ввод
    tokenized_inputs["labels"] = labels
    return tokenized_inputs
  
tokenized_dataset = dataset.map(tokenize_and_align_labels, batched=True)

training_args = TrainingArguments(
    output_dir="./results",
    learning_rate=2e-4,
    per_device_train_batch_size=16,
    per_device_eval_batch_size=16,
    num_train_epochs=3,
    weight_decay=0.01,
    fp16 = True
)

trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_dataset,
    tokenizer=tokenizer,
    data_collator=transformers.default_data_collator,
)

print('Training...')

trainer.train()