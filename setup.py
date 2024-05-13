import json
import os
import requests
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi

def load_api_key(api_key_file):
    with open(api_key_file, 'r') as f:
        api_key_data = json.load(f)
    return api_key_data


api = KaggleApi()

api_key_file = "~/Documents/kaggle/api_key.json"
# Carica la chiave API da file
api_key_data = load_api_key(api_key_file)

# Autentica la sessione Kaggle
api.authenticate(api_key=api_key_data["key"])


# Scarica il dataset specificato dall'URL Kaggle
def download_dataset(dataset_url, output_path):
    # Estrai il nome del dataset dal URL
    dataset_name = dataset_url.split("/")[-1]

    # Scarica il dataset nella directory di output specificata
    api.dataset_download_files(dataset_url, path=output_path, unzip=True)

    # Verifica se il dataset è stato scaricato correttamente
    if os.path.exists(os.path.join(output_path, dataset_name)):
        print("Dataset scaricato con successo.")
    else:
        print("Errore durante il download del dataset.")
def csv_to_dict(csv_file):
    df = pd.read_csv(csv_file)

    data_dict = {}

    for column in df.columns:
        data_dict[column] = df[column].tolist()

    return data_dict


def setup():

    dataset_url = "https://www.kaggle.com/datasets/mohamedabdelwahabali/drugreview/download?datasetVersionNumber=1"
    dataset_save_path = "dataset"
    #csv_file_path = "dataset.csv"

    download_dataset(dataset_url, dataset_save_path)
    #dataset_df = csv_to_dict(csv_file_path)

    return True

if __name__ == "__main__":
    # Eseguire il setup
    dataset = setup()
    # Utilizzare il dataset come necessario
   # print(dataset.head())  # Esemp
