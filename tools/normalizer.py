class Normalizer:
    # These should be right before a word seperated by a half space.
    # TODO: Separate & Classify THESE
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

    def __init__(
            self,
            correct_spacing: bool = True,
            unicodes_replacement: bool = True,
            remove_diacritics: bool = True,
            remove_specials_chars: bool = True,
            persian_numbers: bool = True
    ) -> None:
        self._correct_spacing = correct_spacing
        self._unicodes_replacement = unicodes_replacement
        self._remove_diacritics = remove_diacritics
        self._remove_specials_chars = remove_specials_chars
        self._persian_numbers = persian_numbers

    def normalize(self, text: str) -> str:
        if self._correct_spacing:
            text = Normalizer._correct_spacing(text=text)
        if self._unicodes_replacement:
            text = Normalizer._unicodes_replacement(text=text)
        if self._remove_diacritics:
            text = Normalizer._remove_diacritics(text=text)
        if self._remove_specials_chars:
            text = Normalizer._remove_specials_chars(text=text)
        if self._persian_numbers:
            text = Normalizer._persian_numbers(text=text)
        return text

    @staticmethod
    def _correct_spacing(text: str) -> str:
        return text

    @staticmethod
    def _unicodes_replacement(text: str) -> str:
        return text

    @staticmethod
    def _remove_diacritics(text: str) -> str:
        return text

    @staticmethod
    def _remove_specials_chars(text: str) -> str:
        return text

    @staticmethod
    def _persian_numbers(text: str) -> str:
        return text
