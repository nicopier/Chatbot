from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from sklearn.preprocessing import LabelEncoder
import pickle
import random
import numpy as np

from transformers import GPT2LMHeadModel, GPT2Tokenizer

# Cargamos el Tokenizer y el LabelEncoder guardados durante el entrenamiento
with open('./motor/tokenizer.pickle', 'rb') as handle:
    tokenizer = pickle.load(handle)

with open('./motor/label_encoder.pickle', 'rb') as handle:
    le = pickle.load(handle)

# Cargamos el mapeo de tag a respuestas
with open('./motor/tag_to_responses.pickle', 'rb') as handle:
    tag_to_responses = pickle.load(handle)

max_len = 20
model = load_model('model.h5')

def chat():
    while True:
        print("Usuario: ")
        inp = input()
        if inp.lower() == "quit":
            break

        result = model.predict(pad_sequences(tokenizer.texts_to_sequences([inp]),
                                            truncating='post', maxlen=max_len))
        tag = le.inverse_transform([np.argmax(result)])
        
        # Obtenemos respuesta a partir del tag
        if tag[0] in tag_to_responses:
            response = random.choice(tag_to_responses[tag[0]])
        else:
            response = "Lo siento, no puedo responder a eso."
        
        print("ChatBot: ", response)  # Imprimimos la respuesta en lugar del tag

chat()
