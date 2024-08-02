from index import Index
from whoosh import qparser
from whoosh.scoring import WeightingModel

from functools import reduce
from whoosh.scoring import BM25F


class IRModel:
    def __init__(self, index: Index, weightingModel: WeightingModel = BM25F):
        self.index = index
        self.model = weightingModel
        self.query = ""

    def search(self, query: str, resLimit = -1, sentiments=None, verbose=True):
        resDict = {}
        correctedString = ""
        try:
            # if isinstance(self.model, SentimentModelWA):
            #     self.model.set_user_sentiment(sentiments)
            # elif isinstance(self.model, Doc2VecModel):
            #     self.model.set_query(query)
            s = self.index.indexDrg.searcher(weighting=self.model)
            qp = qparser.MultifieldParser(['drug_name', 'condition', 'review'], schema=self.index.schemaDrg, group=qparser.OrGroup)

            parsedQ = qp.parse(query)
            if (verbose):
                print(f"Input: {query}")
                print(f"Parsed query: {parsedQ}")
            results = s.search(parsedQ, terms=True, limit=resLimit) if resLimit > 0 else s.search(parsedQ, terms=True)
            for i in results:
                resDict[i["id"]] = [i["drug_name"], i["condition"], i['review'], i['rating']]

            # Did you Mean? codice per implementarlo
            # corrected = s.correct_query(parsedQ, query)
            # if corrected.query != parsedQ:
            #     correctedString = reduce(
            #         lambda x, y: x + " " + str(y[1]),
            #         list(filter(lambda term: term[1] if term[0] == "name" else "", corrected.query.iter_all_terms())),
            #         ""
            #     ).strip()
        except Exception as e:
            print(e)
        finally:
            s.close()
        #return correctedString, resDict
        return resDict