import math
import heapq
import pickle
import os


class DocTerm:
    def __init__(self, doc_id: int):
        self.doc_id = doc_id
        self.count = 0
        self.positions = []

    def add_position(self, position: int):
        self.count += 1
        self.positions.append(position)


class Indexer:
    def __init__(self,
                 collection_size: int,
                 load_index: bool = False,
                 postings_list: dict = None,
                 k: int = 10,
                 ):
        if postings_list is None:
            postings_list = dict()

        self.postings_list = postings_list
        self._doc_length = {}
        self._K = k
        self._N = collection_size

        if load_index:
            self.load_index()

    def insert_tokens(self, doc_id: int, tokens: list):
        unique_tokens = set()
        self._doc_length[doc_id] = len(tokens)
        for i in range(len(tokens)):
            token = tokens[i]
            if token not in self.postings_list.keys():
                self.postings_list[token] = (1, [])
                unique_tokens.add(token)

            document_frequency, postings = self.postings_list[token]

            if token not in unique_tokens:
                unique_tokens.add(token)
                document_frequency += 1

            doc_term = None
            if len(postings) > 0:
                doc_term = postings[-1]

            if doc_term is None or doc_term.doc_id != doc_id:
                doc_term = DocTerm(doc_id)
                postings.append(doc_term)

            doc_term.add_position(i)
            self.postings_list[token] = (document_frequency, postings)

    def delete_high_frequency_words(self):
        postings_list = self.postings_list
        document_frequencies = [(postings_list[term][0], term) for term in postings_list.keys()]
        document_frequencies.sort(reverse=True)

        for i in range(min(50, len(document_frequencies))):
            term = document_frequencies[i][1]
            print(term, postings_list[term][0])
            self.postings_list.pop(term, None)

    # Make an indexer with the highest term frequencies
    def get_champions_list(self) -> 'Indexer':
        ...

    def process_query(self, query: list) -> list:
        postings_list = self.postings_list
        scores = {}
        for term in query:
            document_frequency, postings = postings_list[term]
            for posting in postings:
                tf = posting.count
                doc_id = posting.doc_id
                if doc_id not in scores:
                    scores[doc_id] = 0.0
                scores[doc_id] += Indexer.tf_calculation(tf) * self.df_calculation(document_frequency)

        scores = self.normalizer(scores)
        top_k = heapq.nlargest(self._K, scores.items(), key=lambda x: x[1])

        return [(doc_id, score) for doc_id, score in top_k]

    def save_index(self):
        with open('./collection/indexer.pkl', 'wb') as file:
            pickle.dump(self, file)

    @staticmethod
    def load_index():
        file_path = './collection/indexer.pkl'

        if os.path.exists(file_path):
            with open(file_path, 'rb') as file:
                return pickle.load(file)

        else:
            return False

    @staticmethod
    def tf_calculation(tf: int) -> float:
        return 1 + math.log(tf)

    def df_calculation(self, df: int):
        return 1 + math.log(self._N / float(df))

    def normalizer(self, scores: dict):
        for doc_id in scores.keys():
            scores[doc_id] /= self._doc_length[doc_id]
        return scores
