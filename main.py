import json
from tools import WordTokenizer, Normalizer, Indexer
from hazm import Stemmer


def get_collection():
    dirty_collection = json.load(open("collection/IR_data_news_12k.json", "r"))
    return {int(doc_id): dirty_collection[doc_id] for doc_id in dirty_collection.keys()}


def process_text(text: str) -> list:
    normalized_text = normalizer.normalize(text=text)
    tokens = tokenizer.tokenize(text=normalized_text)
    for i in range(len(tokens)):
        tokens[i] = stemmer.stem(tokens[i].lower())
    return tokens


collection = get_collection()
normalizer = Normalizer()
tokenizer = WordTokenizer()
stemmer = Stemmer()

positional_inverted_index = Indexer(collection_size=len(collection.keys()))


for document_id, document in collection.items():
    cleaned_tokens = process_text(collection[document_id]["content"])
    positional_inverted_index.insert_tokens(document_id, cleaned_tokens)

positional_inverted_index.delete_high_frequency_words()
positional_inverted_index.save_index()

queries = []

for query in queries:
    cleaned_query = process_text(query)
    print(f"Query: {query} \n", positional_inverted_index.process_query(query))
