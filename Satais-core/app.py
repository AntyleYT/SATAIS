import numpy as np
import tensorflow as tf


model = tf.keras.models.load_model('trained_model')


with open('database.txt', 'r', encoding='utf-8') as f:
    data = f.read()

tokenizer = tf.keras.preprocessing.text.Tokenizer()
tokenizer.fit_on_texts([data])


def generate_text(seed_text, next_words, model, tokenizer):
    for _ in range(next_words):
        token_list = tokenizer.texts_to_sequences([seed_text])[0]
        token_list = np.array(token_list)
        token_list = np.reshape(token_list, (1, 1, 1))
        predicted = model.predict_classes(token_list, verbose=0)
        output_word = ""
        for word, index in tokenizer.word_index.items():
            if index == predicted:
                output_word = word
                break
        seed_text += " " + output_word
    return seed_text

while True:
    user_input = input("User: ")
    response = generate_text(user_input, 100, model, tokenizer)
    print("Python(l'IA):", response)
