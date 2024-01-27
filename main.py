import json
from tools import Tokenizer, Normalizer


def get_collection():
    dirty_collection = json.load(open("collection/IR_data_news_12k.json", "r"))
    return {int(doc_id): dirty_collection[doc_id] for doc_id in dirty_collection.keys()}


collection = get_collection()

tokenizer = Tokenizer()
normalizer = Normalizer()

postings_list = {}

for document_id, document in collection.items():
    normalized_text = normalizer.normalize(text=collection[document_id]["content"])
    tokens = tokenizer.tokenize(text=collection[document_id]["content"])
