import json
from tools import Tokenizer, Normalizer


def get_collection():
    dirty_collection = json.load(open("collection/IR_data_news_12k.json", "r"))
    return {int(doc_id): dirty_collection[doc_id] for doc_id in dirty_collection.keys()}


collection = get_collection()

tokenizer = Tokenizer([""])
normalizer = Normalizer(numbers=True)

tokens = []
for document_id, document in collection.items():
    # for token in tokenizer.tokenize(collection[document_id]["content"]):
    #     tokens.append((token, document_id))
    print(normalizer.normalize(text=collection[document_id]["content"]))
