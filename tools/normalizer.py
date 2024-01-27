import re
from hazm import Normalizer

# These should be right before a word seperated by a half space.
SPACING_PATTERN = ['ی', 'ای', 'ها', 'های', 'تر', 'تری', 'ترین', 'گر', 'گری', 'ام', 'ات', 'اش', 'اعداد', 'می', 'نمی']

# The english numbers within the text should be converted into persian numbers.
NUMBERS = {
    ord('0'): '۰',
    ord('1'): '۱',
    ord('2'): '۲',
    ord('3'): '۳',
    ord('4'): '۴',
    ord('5'): '۵',
    ord('6'): '۶',
    ord('7'): '۷',
    ord('8'): '۸',
    ord('9'): '۹',
}

# FATHATAN, DAMMATAN, KASRATAN, FATHA, DAMMA, KASRA, SHADDA, SUKUN

STOP_WORDS = []

SPECIAL_WORDS = {
    "﷽": "بسم الله الرحمن الرحیم",
    "﷼": "ریال",
    "(ﷰ|ﷹ)": "صلی",
    "ﷲ": "الله",
    "ﷳ": "اکبر",
    "ﷴ": "محمد",
    "ﷵ": "صلعم",
    "ﷶ": "رسول",
    "ﷷ": "علیه",
    "ﷸ": "وسلم",
    "ﻵ|ﻶ|ﻷ|ﻸ|ﻹ|ﻺ|ﻻ|ﻼ": "لا"
}


class Normalizer:
    _spacing = True
    _numbers = True
    _stop = True
    _special = True
    _unnecessary = True

    def __init__(self, spacing=False, numbers=False, patterns=[]) -> None:
        self._spacing = spacing
        self._numbers = numbers
        self.patterns = patterns

    def normalize(self, text: str) -> str:
        if self._numbers:
            text = self.normalize_numbers(text)
        return text

    @staticmethod
    def normalize_numbers(text: str) -> str:
        return text.translate(NUMBERS)

    @staticmethod
    def special_words(text: str) -> str:
        for special in SPECIAL_WORDS:
            return re.sub(r'special', '', text)
