import json
import os

def load_json(file_path):
    if not os.path.exists(file_path):
        return []
    with open(file_path, 'r', encoding='utf-8') as f:
        try:
            return json.load(f)
        except:
            return []

def save_json(file_path, data):
    with open(file_path, 'w', encoding='utf-8') as f:
        json.dump(data, f, indent=4, ensure_ascii=False)

def load_clients():
    return load_json("data/clients.json")

def save_clients(clients_list):
    save_json("data/clients.json", clients_list)

def load_factures():
    return load_json("data/factures.json")

def save_factures(factures_list):
    save_json("data/factures.json", factures_list)
