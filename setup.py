import json
import os
import requests
import pandas as pd
from kaggle.api.kaggle_api_extended import KaggleApi

def load_api_key(api_key_file):
    with open(api_key_file, 'r') as f:
        api_key_data = json.load(f)
    return api_key_data


# Scarica il dataset specificato dall'URL Kaggle
def download_dataset(dataset_url, output_path):
    if len(os.listdir(output_path)):
        print("Dataset already exists, or directory is not empty. Skipping download.")
        return
    api = KaggleApi()
    try:
        api.authenticate()
    except:
        print("Authentication Faild")

    api.dataset_download_files(dataset_url, path=output_path, unzip=True)
    if len(os.listdir(output_path)):
        print("Dataset scaricato con successo.")
    else:
        print("Errore durante il download del dataset.")

def csv_to_list_of_dicts(csv_file):
    df = pd.read_csv(csv_file)

    data_list = []
    count = 0
    for _, row in df.iterrows():
        row_dict = {
            'id': count,
            'patient_id': row['patient_id'],
            'drugName': row['drugName'],
            'condition': row['condition'],
            'review': row['review'],
            'rating': row['rating'],
            'date': row['date'],
            'usefulCount': row['usefulCount'],
            'review_length': len(row['review'])
        }
        count += 1
        data_list.append(row_dict)

    return data_list


def setup():

    dataset_url = "mohamedabdelwahabali/drugreview"
    dataset_save_path = "dataset"
    download_dataset(dataset_url, dataset_save_path)
    csv_file_path = os.path.join(dataset_save_path, 'drug_review_train.csv')
    dataset_df = csv_to_list_of_dicts(csv_file_path)

    return dataset_df

if __name__ == "__main__":
    dataset = setup()
    print(dataset)
