from tqdm import tqdm
import yaml, os
import json

from whoosh.fields import Schema, TEXT, ID, NUMERIC
from whoosh import index


class Index():

    def __init__(self, forceBuildIndex=False, limit=None):
        self.schemaDrg = self.setupschemaDrg()
        self.indexDrg = self.setupindexDrg(forceBuildIndex, limit)

    def setupschemaDrg(self):
        schema = Schema(
            id=ID(stored=True, unique=True),
            patient_id=NUMERIC(stored=True, unique=False),
            drug_name=TEXT(stored=True, field_boost=2.0, spelling=True),
            condition=TEXT(stored=True, field_boost=2.0, spelling=True),
            review=TEXT(stored=True),
            date_of_review=TEXT(stored=True),
            rating=NUMERIC(stored=True, numtype=float),
            useful_count=NUMERIC(stored=True, numtype=float),
        )
        return schema

    def setupindexDrg(self, forceBuildIndex, limit):
        with open('config.yaml', 'r') as file:
            config_data = yaml.safe_load(file)

        if not os.path.exists(f"{config_data['INDEX']['MAINDIR']}/{config_data['INDEX']['DRGINDX']}") or forceBuildIndex:
            return self.createindexDrg(limit)
        else:
            return index.open_dir(f"{config_data['INDEX']['MAINDIR']}/{config_data['INDEX']['DRGINDX']}")

    # def createindexDrg(self, limit):
    #
    #     with open('config.yaml', 'r') as file:
    #         config_data = yaml.safe_load(file)
    #     try:
    #         if not os.path.exists(f"{config_data['INDEX']['MAINDIR']}"):
    #             os.mkdir(f"{config_data['INDEX']['MAINDIR']}")
    #
    #         os.mkdir(f"{config_data['INDEX']['MAINDIR']}/{config_data['INDEX']['DRGINDX']}")
    #     except FileExistsError:
    #         pass
    #
    #     data_dir = f"./{config_data['DATA']['DATADIR']}"
    #     ix = index.create_in(f"{config_data['INDEX']['MAINDIR']}/{config_data['INDEX']['DRGINDX']}", self.schemaDrg)
    #     writer = ix.writer()
    #     line_count = 0
    #     for jsonFile in os.listdir(data_dir):
    #         with open(u"{dir}/{file}".format(dir=data_dir, file=jsonFile), "r", encoding="utf-8") as file:
    #             for line in file:
    #                 json_obj = json.loads(line)
    #                 writer.add_document(
    #                     id=str(line_count),
    #                     patient_id=json_obj.get('patient_id', ''),
    #                     drug_name=json_obj.get('drugName', ''),
    #                     condition=json_obj.get('condition', ''),
    #                     review=json_obj.get('review', ''),
    #                     date_of_review=json_obj.get('date', ''),
    #                     rating=json_obj.get('rating', ''),
    #                     useful_count=json_obj.get('usefulCount', '')
    #                 )
    #                 line_count += 1
    #                 if limit and line_count > limit:
    #                     writer.commit()
    #                     return ix
    #     writer.commit()
    #     return ix

    def createindexDrg(self, limit):
        with open('config.yaml', 'r') as file:
            config_data = yaml.safe_load(file)
        try:
            if not os.path.exists(f"{config_data['INDEX']['MAINDIR']}"):
                os.mkdir(f"{config_data['INDEX']['MAINDIR']}")
            os.mkdir(f"{config_data['INDEX']['MAINDIR']}/{config_data['INDEX']['DRGINDX']}")
        except FileExistsError:
            pass

        data_dir = f"./{config_data['DATA']['DATADIR']}"
        ix = index.create_in(f"{config_data['INDEX']['MAINDIR']}/{config_data['INDEX']['DRGINDX']}", self.schemaDrg)
        writer = ix.writer()
        line_count = 0

        json_files = os.listdir(data_dir)

        with tqdm(total=len(json_files), desc="File processati", unit="file", leave=False) as pbar_file:
            for jsonFile in json_files:
                with open(os.path.join(data_dir, jsonFile), "r", encoding="utf-8") as file:
                    lines = file.readlines()
                    with tqdm(total=len(lines), desc="", unit="line", leave=False, position=1) as pbar_line:
                        for line in lines:
                            json_obj = json.loads(line)
                            writer.add_document(
                                id=str(line_count),
                                patient_id=json_obj.get('patient_id', ''),
                                drug_name=json_obj.get('drugName', ''),
                                condition=json_obj.get('condition', ''),
                                review=json_obj.get('review', ''),
                                date_of_review=json_obj.get('date', ''),
                                rating=json_obj.get('rating', ''),
                                useful_count=json_obj.get('usefulCount', '')
                            )
                            line_count += 1
                            pbar_line.update(1)
                            if limit and line_count > limit:
                                writer.commit()
                                return ix
                pbar_file.update(1)

        writer.commit()
        return ix


if __name__ == '__main__':
    my_index = Index(forceBuildIndex=False, limit=10000)

