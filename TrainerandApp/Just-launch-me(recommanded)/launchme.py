
import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

model = load_model('default-sataismodelv1.h5')
with open('tokenizer.pkl', 'rb') as file:
    tokenizer = pickle.load(file)

def generate_response(seed_text, max_words):
    seed_sequence = tokenizer.texts_to_sequences([seed_text])[0]
    seed_sequence = pad_sequences([seed_sequence], maxlen=4, padding='pre')

    response = []
    for _ in range(max_words):
        predicted = model.predict_classes(seed_sequence, verbose=0)
        output_word = ""
        for word, index in tokenizer.word_index.items():
            if index == predicted:
                output_word = word
                break
        seed_sequence = np.append(seed_sequence, predicted)
        seed_sequence = seed_sequence[1:]
        response.append(output_word)

    return ' '.join(response)

print("SATAIS: Hello , I'm SATAIS , created by Antyle_YT and HAISDIP ! Ask me sometimes and I give you the responce! ")
while True:
    user_input = input("User (You): ")

    input_sequence = user_input.lower().strip()
    response = generate_response(input_sequence, max_words=10)

    print(f"SATAIS: {response.capitalize()}")
