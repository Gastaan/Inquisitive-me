class Term:
    ...


class Indexer:
    def __init__(self, load_index: bool = False, similarity_function: str = 'cosine'):
        self._similarity_function = similarity_function
        self._postings_list = dict()

        if load_index:
            self.load_index()

    def insert_tokens(self, tokens: list):
        for i in range(len(tokens)):
            token = tokens[i]
            if token not in self._postings_list.keys():
                self._postings_list[token] = (1, list())

    def process_query(self, query: str) -> list:
        ...

    def save_index(self):
        ...

    def load_index(self):
        ...
