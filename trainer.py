import numpy as np
import tensorflow as tf

batch_size = 64
epochs = 50
latent_dim = 256
num_samples = 10000

with open('database.txt', 'r', encoding='utf-8') as f:
    data = f.read()


tokenizer = tf.keras.preprocessing.text.Tokenizer()
tokenizer.fit_on_texts([data])
vocab_size = len(tokenizer.word_index) + 1
sequences = tokenizer.texts_to_sequences([data])[0]


input_sequences = []
output_sequences = []
for i in range(0, len(sequences) - 1):
    input_sequences.append(sequences[i])
    output_sequences.append(sequences[i + 1])


input_sequences = np.array(input_sequences)
output_sequences = np.array(output_sequences)

input_sequences = np.reshape(input_sequences, (len(input_sequences), 1, 1))

model = tf.keras.Sequential([
    tf.keras.layers.LSTM(latent_dim, input_shape=(1, 1)),
    tf.keras.layers.Dense(vocab_size, activation='softmax')
])

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam')

model.fit(input_sequences, output_sequences, batch_size=batch_size, epochs=epochs)

model.save('trained_model.keras')
