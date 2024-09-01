import tensorflow as tf
import numpy as np
import os
import pickle
from tensorflow.keras.preprocessing.text import Tokenizer

seq_length = 100
embedding_dim = 256
rnn_units = 1024
batch_size = 64
buffer_size = 10000
epochs = 50  # Nombre d'époques

# Charger et préparer le corpus de texte
path_to_file = 'corpus.txt'
text = open(path_to_file, 'rb').read().decode(encoding='utf-8')

# Initialiser le tokenizer Stoken et ajuster sur le texte
Stoken = Tokenizer()
Stoken.fit_on_texts([text])
total_words = len(Stoken.word_index) + 1  # Nombre total de mots uniques + 1 pour OOV

# Vectoriser le texte
text_as_int = Stoken.texts_to_sequences([text])[0]

# Créer des séquences d'entraînement
char_dataset = tf.data.Dataset.from_tensor_slices(text_as_int)

sequences = char_dataset.batch(seq_length + 1, drop_remainder=True)

def split_input_target(chunk):
    input_text = chunk[:-1]
    target_text = chunk[1:]
    return input_text, target_text

dataset = sequences.map(split_input_target)

# Mélanger et préparer par batch
dataset = dataset.shuffle(buffer_size).batch(batch_size, drop_remainder=True)

# Construire le modèle
def build_model(vocab_size, embedding_dim, rnn_units, batch_size):
    model = tf.keras.Sequential([
        tf.keras.layers.Embedding(vocab_size, embedding_dim),
        tf.keras.layers.LSTM(rnn_units, return_sequences=True, stateful=False, recurrent_initializer='glorot_uniform'),
        tf.keras.layers.Dense(vocab_size)
    ])
    return model

model = build_model(vocab_size=total_words, embedding_dim=embedding_dim, rnn_units=rnn_units, batch_size=batch_size)

# Définir la fonction de perte
def loss(labels, logits):
    return tf.keras.losses.sparse_categorical_crossentropy(labels, logits, from_logits=True)

model.compile(optimizer='adam', loss=loss)

# Entraîner le modèle
checkpoint_dir = './training_checkpoints'
checkpoint_prefix = os.path.join(checkpoint_dir, "ckpt_{epoch}.weights.h5")

checkpoint_callback = tf.keras.callbacks.ModelCheckpoint(
    filepath=checkpoint_prefix,
    save_weights_only=True
)

history = model.fit(dataset, epochs=epochs, callbacks=[checkpoint_callback])

# Enregistrer le modèle entraîné
model.save('sataismodelv2.h5')

# Sauvegarder le tokenizer Stoken
with open('Stoken.pkl', 'wb') as file:
    pickle.dump(Stoken, file)

print("Training finished , file name : 'customsataismodel.py'")
