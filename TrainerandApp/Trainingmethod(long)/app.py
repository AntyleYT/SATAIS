import numpy as np
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
import pickle

# Charger le modèle sans le compiler
model = load_model('sataismodelv2.h5', compile=False)

# Charger le tokenizer Stoken
with open('Stoken.pkl', 'rb') as file:
    Stoken = pickle.load(file)


def generate_response(seed_text, max_words):
    # Convertir le texte de départ en séquence d'indices
    seed_sequence = Stoken.texts_to_sequences([seed_text])[0]
    seed_sequence = pad_sequences([seed_sequence], maxlen=4, padding='pre')

    response = []
    for _ in range(max_words):
        # Prédire l'indice du prochain mot
        predicted = np.argmax(model.predict(seed_sequence), axis=-1)[0]

        # Trouver le mot correspondant à l'indice prédit
        for word, index in Stoken.word_index.items():
            if index == predicted:
                response.append(word)
                break

        # Mettre à jour la séquence de départ pour la prochaine prédiction
        seed_sequence = np.append(seed_sequence, predicted)
        seed_sequence = seed_sequence[1:].reshape(1, -1)

    return ' '.join(response)


print("SATAIS: Hello, I'm SATAIS, created by Antyle_YT and HAISDIP! Ask me something and I'll give you a response!")
while True:
    user_input = input("User (You): ")

    input_sequence = user_input.lower().strip()
    response = generate_response(input_sequence, max_words=100)

    print(f"SATAIS: {response.capitalize()}")
