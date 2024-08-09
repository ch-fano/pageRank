import json
import os
import shutil
from collections import OrderedDict
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

        # Aggiungi l'ID univoco a ciascun documento JSONL
        add_unique_id_to_jsonl_files(json_folder)
    else:
        print("Errore durante il download del dataset.")


def add_unique_id_to_jsonl_files(json_folder):
    id_counter = 1  # Contatore iniziale per l'ID univoco

    # Itera su ogni file JSONL nella cartella json/
    for file_name in os.listdir(json_folder):
        if file_name.endswith('.jsonl'):
            file_path = os.path.join(json_folder, file_name)
            temp_file_path = file_path + ".tmp"

            with open(file_path, 'r', encoding='utf-8') as f_in, open(temp_file_path, 'w', encoding='utf-8') as f_out:
                for line in f_in:
                    try:
                        json_obj = json.loads(line)

                        # Creare un nuovo dizionario con l'ID come primo campo
                        ordered_json_obj = OrderedDict()
                        ordered_json_obj['id'] = id_counter  # Aggiunge l'ID univoco

                        # Aggiunge gli altri campi mantenendo l'ordine originale
                        for key, value in json_obj.items():
                            ordered_json_obj[key] = value

                        f_out.write(json.dumps(ordered_json_obj) + '\n')
                        id_counter += 1
                    except json.JSONDecodeError as e:
                        print(f"Errore nel parsing del JSON nel file {file_name}: {e}")

            # Sovrascrive il file originale con il file temporaneo aggiornato
            shutil.move(temp_file_path, file_path)

    print("Campo 'id' aggiunto a tutti i documenti JSONL come primo campo.")


def setup():
    dataset_url = "mohamedabdelwahabali/drugreview"
    dataset_save_path = "dataset"
    download_dataset(dataset_url, dataset_save_path)


if __name__ == "__main__":
    setup()
