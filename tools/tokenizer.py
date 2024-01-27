import re


class Tokenizer:
    def __init__(self, configs: list):
        self.configs = configs

    def tokenize(self, text: str) -> list:
        return re.split(r'\s+', text.strip())
