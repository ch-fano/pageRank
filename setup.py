import json
import os
import shutil
from kaggle.api.kaggle_api_extended import KaggleApi

def load_api_key(api_key_file):
    with open(api_key_file, 'r') as f:
        api_key_data = json.load(f)
    return api_key_data

# Scarica il dataset specificato dall'URL Kaggle
def download_dataset(dataset_url, output_path):
    # Crea la cartella output_path se non esiste
    if not os.path.exists(output_path):
        os.makedirs(output_path)

    if len(os.listdir(output_path)):
        print("Dataset already exists, or directory is not empty. Skipping download.")
        return
    api = KaggleApi()
    try:
        api.authenticate()
    except:
        print("Authentication Failed")

    api.dataset_download_files(dataset_url, path=output_path, unzip=True)

    if len(os.listdir(output_path)):
        print("Dataset scaricato con successo.")
        # Creazione della cartella json/ se non esiste
        json_folder = os.path.join(output_path, 'json')
        if not os.path.exists(json_folder):
            os.makedirs(json_folder)
        # Sposta tutti i file JSON nella cartella json/
        for file_name in os.listdir(output_path):
            if file_name.endswith('.jsonl'):
                shutil.move(os.path.join(output_path, file_name), os.path.join(json_folder, file_name))
        print(f"Tutti i file JSON sono stati spostati nella cartella '{json_folder}'.")
    else:
        print("Errore durante il download del dataset.")

def setup():
    dataset_url = "mohamedabdelwahabali/drugreview"
    dataset_save_path = "dataset"
    download_dataset(dataset_url, dataset_save_path)

if __name__ == "__main__":
    setup()
