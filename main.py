import json

from parsivar import FindStems
from hazm import WordTokenizer, Normalizer
from indexer import Indexer


def get_collection():
    dirty_collection = json.load(open("collection/IR_data_news_5k.json", "r"))
    return {int(d_id): dirty_collection[d_id] for d_id in dirty_collection.keys()}


stop_words = ['.', '،', '/', '«', '»', '', ':', '(', ')', '\'', '*', '-', ',', '=', '_']
s_words = ['و', 'به', 'در', 'با', 'این', 'اگر', 'از', '', 'را', 'چه', 'برای', 'همین', 'آن', 'تا', '@', 'که', 'هم']


def delete_stop_words(tokens: list):
    finally_cleaned_tokens = []
    for i in range(len(tokens)):
        for j in range(10 * len(stop_words)):
            for stopword in stop_words:
                tokens[i] = tokens[i].strip(stopword)
        if tokens[i] not in s_words and len(tokens[i]) > 1:
            finally_cleaned_tokens.append(tokens[i])
    return finally_cleaned_tokens


def process_text(text: str) -> list:
    # print("Raw text:", text)
    normalized_text = normalizer.normalize(text=text)
    # print("Normalized Text:", normalized_text)
    tokens = delete_stop_words(tokenizer.tokenize(text=normalized_text))
    # print("Tokens:", tokens)
    for i in range(len(tokens)):
        tokens[i] = stemmer.convert_to_stem(tokens[i].lower())
    # print("Tokens After Stemming:", tokens)
    return tokens


collection = get_collection()
normalizer = Normalizer()
tokenizer = WordTokenizer()
stemmer = FindStems()

positional_inverted_index = Indexer.load_index()

if not positional_inverted_index:
    positional_inverted_index = Indexer(collection_size=len(collection.keys()))

    for document_id in sorted(collection.keys()):
        cleaned_tokens = process_text(collection[document_id]["content"])
        positional_inverted_index.insert_tokens(document_id, cleaned_tokens)

    positional_inverted_index.delete_high_frequency_words()
    positional_inverted_index.create_champions_list()

    positional_inverted_index.save_index()


queries = ["خبر", "بازیابی", "قرن ۱۴", "اخبار فوتبال"]
for query in queries:
    cleaned_query = process_text(query)
    print(f"Query: {query} \n")
    related_docs = positional_inverted_index.process_query(cleaned_query)
    for z in range(5):
        related_doc = related_docs[z]
        (doc_id, score) = related_doc
        print(collection[doc_id], '\n_____________________\n')
