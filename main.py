import json
from tools import Indexer
from hazm import Stemmer, WordTokenizer, Normalizer


def get_collection():
    dirty_collection = json.load(open("collection/IR_data_news_12k.json", "r"))
    return {int(d_id): dirty_collection[d_id] for d_id in dirty_collection.keys()}


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

positional_inverted_index = Indexer.load_index()

if not positional_inverted_index:
    positional_inverted_index = Indexer(collection_size=len(collection.keys()))

    for document_id in sorted(collection.keys()):
        cleaned_tokens = process_text(collection[document_id]["content"])
        positional_inverted_index.insert_tokens(document_id, cleaned_tokens)

    positional_inverted_index.delete_high_frequency_words()
    positional_inverted_index.create_champions_list()

    positional_inverted_index.save_index()

queries = ["سامان"]

for query in queries:
    cleaned_query = process_text(query)
    print(f"Query: {query} \n")
    related_docs = positional_inverted_index.process_query(cleaned_query)
    for related_doc in related_docs:
        (doc_id, score) = related_doc
        print(collection[doc_id], '\n_____________________\n')
