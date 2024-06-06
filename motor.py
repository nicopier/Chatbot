import json
import tensorflow as tf
from tensorflow import keras
from sklearn.preprocessing import LabelEncoder
import numpy as np
import pandas as pd
import pickle
from tensorflow.keras.preprocessing.text import Tokenizer
from tensorflow.keras.preprocessing.sequence import pad_sequences

with open('./data.json') as f:
    data = json.load(f)

training_sentences = []
training_labels = []
labels = []
tag_to_responses = {}  # Newly added

for intent in data['intents']:
    for pattern in intent['patterns']:
        training_sentences.append(pattern)
        training_labels.append(intent['tag'])
    responses = intent['responses']  # Moved inside the loop
    if intent['tag'] not in labels:
        labels.append(intent['tag'])
    
    tag_to_responses[intent['tag']] = responses  # Create a mapping from tag to responses

encoder = LabelEncoder()
encoder.fit(training_labels)
training_labels = encoder.transform(training_labels)

# Guardar LabelEncoder
with open('label_encoder.pickle', 'wb') as le_dump_file:
    pickle.dump(encoder, le_dump_file)

num_classes = len(set(training_labels))
vocab_size = 1000
embedding_dim = 16
max_len = 20
oov_token = "<OOV>"

tokenizer = Tokenizer(num_words=vocab_size, oov_token=oov_token)
tokenizer.fit_on_texts(training_sentences)

# Guardar Tokenizer
with open('tokenizer.pickle', 'wb') as tok_dump_file:
    pickle.dump(tokenizer, tok_dump_file)

sequences = tokenizer.texts_to_sequences(training_sentences)
padded_sequences = pad_sequences(sequences, truncating='post', maxlen=max_len)

model = tf.keras.models.Sequential([
    tf.keras.layers.Embedding(vocab_size, embedding_dim, input_length=max_len),
    tf.keras.layers.GlobalAveragePooling1D(),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(16, activation='relu'),
    tf.keras.layers.Dense(num_classes, activation='softmax')
])

model.compile(loss='sparse_categorical_crossentropy', optimizer='adam', metrics=['accuracy'])

model.fit(padded_sequences, np.array(training_labels), epochs=50)

# Guardar tag_to_responses
with open('tag_to_responses.pickle', 'wb') as tr_dump_file:
    pickle.dump(tag_to_responses, tr_dump_file)

model.save('./motor/model.h5')
