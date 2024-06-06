from telethon.sync import TelegramClient
from telethon.tl.functions.messages import GetDialogsRequest
from telethon.tl.types import InputPeerEmpty
import csv

api_id = 28223221
api_hash = 'd4c4075f423fae013fabac8ea7f37727'
phone = '+543402496679'

client = TelegramClient(phone, api_id, api_hash)
client.start()

# Obtenemos todos los grupos.
groups = {g.entity.title: g.entity for g in client.get_dialogs() if g.is_group}

# Imprimimos los nombres de los grupos.
for i, title in enumerate(groups.keys(), start=1):
    print(f"{i}. {title}")

# Pedimos un input al usuario para escoger un grupo.
group_number = int(input("Por favor, introduce el número del grupo del que quieres descargar los mensajes: "))
group_title = list(groups.keys())[group_number-1]

# Obtenemos los mensajes del grupo seleccionado.
all_messages = client.get_messages(groups[group_title], limit=None)  # limit=None para obtener todos los mensajes

# Guardamos los mensajes en un archivo de texto.  
with open(f'{group_title}.txt', 'w', encoding="utf-8-sig") as f:
    for msg in all_messages:
        # Obtenemos el nombre del sender a partir del sender_id.
        sender = client.get_entity(msg.sender_id)
        f.write(f"{sender.first_name if sender.first_name else ''} {sender.last_name if sender.last_name else ''}: {msg.text}\n")
