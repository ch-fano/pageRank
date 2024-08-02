from index import Index
from model import IRModel

if __name__ == '__main__':
    my_index = Index()
    model = IRModel(my_index)
    resDict = model.search('birth control', resLimit=10000)
    for res in resDict:
        print(resDict[res])
    print("LEN: ", len(resDict))