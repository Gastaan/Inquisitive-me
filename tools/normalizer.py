import re
from hazm import WordTokenizer, Lemmatizer


class Normalizer:
    # # These should be right before a word seperated by a half space.
    # # TODO: Separate & Classify THESE
    # SPACING_PATTERN = ['ی', 'ای', 'ها', 'های', 'تر', 'تری', 'ترین', 'گر', 'گری', 'ام', 'ات', 'اش', 'اعداد', 'می', 'نمی']
    #
    # # The english numbers within the text should be converted into persian numbers.
    # NUMBERS = {
    #     ord('0'): '۰',
    #     ord('1'): '۱',
    #     ord('2'): '۲',
    #     ord('3'): '۳',
    #     ord('4'): '۴',
    #     ord('5'): '۵',
    #     ord('6'): '۶',
    #     ord('7'): '۷',
    #     ord('8'): '۸',
    #     ord('9'): '۹',
    # }
    #
    # SPECIAL_WORDS = {
    #     "﷽": "بسم الله الرحمن الرحیم",
    #     "﷼": "ریال",
    #     "(ﷰ|ﷹ)": "صلی",
    #     "ﷲ": "الله",
    #     "ﷳ": "اکبر",
    #     "ﷴ": "محمد",
    #     "ﷵ": "صلعم",
    #     "ﷶ": "رسول",
    #     "ﷷ": "علیه",
    #     "ﷸ": "وسلم",
    #     "ﻵ|ﻶ|ﻷ|ﻸ|ﻹ|ﻺ|ﻻ|ﻼ": "لا"
    # }

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

        self.number_translation_src = "0123456789%٠١٢٣٤٥٦٧٨٩"
        self.number_translation_dst = "۰۱۲۳۴۵۶۷۸۹٪۰۱۲۳۴۵۶۷۸۹"

        self.translation_src = "ؠػػؽؾؿكيٮٯٷٸٹٺٻټٽٿڀځٵٶٷٸٹٺٻټٽٿڀځڂڅڇڈډڊڋڌڍڎڏڐڑڒړڔڕږڗڙښڛڜڝڞڟڠڡڢڣڤڥڦڧڨڪګڬڭڮڰڱڲڳڴڵڶڷڸڹںڻڼڽھڿہۂۃۄۅۆۇۈۉۊۋۏۍێېۑےۓەۮۯۺۻۼۿݐݑݒݓݔݕݖݗݘݙݚݛݜݝݞݟݠݡݢݣݤݥݦݧݨݩݪݫݬݭݮݯݰݱݲݳݴݵݶݷݸݹݺݻݼݽݾݿࢠࢡࢢࢣࢤࢥࢦࢧࢨࢩࢪࢫࢮࢯࢰࢱࢬࢲࢳࢴࢶࢷࢸࢹࢺࢻࢼࢽﭐﭑﭒﭓﭔﭕﭖﭗﭘﭙﭚﭛﭜﭝﭞﭟﭠﭡﭢﭣﭤﭥﭦﭧﭨﭩﭮﭯﭰﭱﭲﭳﭴﭵﭶﭷﭸﭹﭺﭻﭼﭽﭾﭿﮀﮁﮂﮃﮄﮅﮆﮇﮈﮉﮊﮋﮌﮍﮎﮏﮐﮑﮒﮓﮔﮕﮖﮗﮘﮙﮚﮛﮜﮝﮞﮟﮠﮡﮢﮣﮤﮥﮦﮧﮨﮩﮪﮫﮬﮭﮮﮯﮰﮱﺀﺁﺃﺄﺅﺆﺇﺈﺉﺊﺋﺌﺍﺎﺏﺐﺑﺒﺕﺖﺗﺘﺙﺚﺛﺜﺝﺞﺟﺠﺡﺢﺣﺤﺥﺦﺧﺨﺩﺪﺫﺬﺭﺮﺯﺰﺱﺲﺳﺴﺵﺶﺷﺸﺹﺺﺻﺼﺽﺾﺿﻀﻁﻂﻃﻄﻅﻆﻇﻈﻉﻊﻋﻌﻍﻎﻏﻐﻑﻒﻓﻔﻕﻖﻗﻘﻙﻚﻛﻜﻝﻞﻟﻠﻡﻢﻣﻤﻥﻦﻧﻨﻩﻪﻫﻬﻭﻮﻯﻰﻱﻲﻳﻴىكي“” "
        self.translation_dst = (
            'یککیییکیبقویتتبتتتبحاوویتتبتتتبحححچدددددددددررررررررسسسصصطعففففففققکککککگگگگگللللنننننهچهههوووووووووییییییهدرشضغهبببببببححددرسعععففکککممنننلررسححسرحاایییووییحسسکببجطفقلمییرودصگویزعکبپتریفقنااببببپپپپببببتتتتتتتتتتتتففففححححححححچچچچچچچچددددددددژژررککککگگگگگگگگگگگگننننننههههههههههییییءاااووااییییااببببتتتتثثثثججججححححخخخخددذذررززسسسسششششصصصصضضضضططططظظظظععععغغغغففففققققککککللللممممننننههههوویییییییکی"" '
        )

        self.diacritics_patterns = [
            # remove FATHATAN, DAMMATAN, KASRATAN, FATHA, DAMMA, KASRA, SHADDA, SUKUN
            ("[\u064b\u064c\u064d\u064e\u064f\u0650\u0651\u0652]", ""),
        ]

        self.suffixes = {
            "ی",
            "ای",
            "ها",
            "های",
            "هایی",
            "تر",
            "تری",
            "ترین",
            "گر",
            "گری",
            "ام",
            "ات",
            "اش",
        }

        self.extra_space_patterns = [
            (r" {2,}", " "),  # remove extra spaces
            (r"\n{3,}", "\n\n"),  # remove extra newlines
            (r"\u200c{2,}", "\u200c"),  # remove extra ZWNJs
            (r"\u200c{1,} ", " "),  # remove unneded ZWNJs before space
            (r" \u200c{1,}", " "),  # remove unneded ZWNJs after space
            (r"\b\u200c*\B", ""),  # remove unneded ZWNJs at the beginning of words
            (r"\B\u200c*\b", ""),  # remove unneded ZWNJs at the end of words
            (r"[ـ\r]", ""),  # remove keshide, carriage returns
        ]

        punc_after, punc_before = r"\.:!،؛؟»\]\)\}", r"«\[\(\{"

        self.punctuation_spacing_patterns = [
            # remove space before and after quotation
            ('" ([^\n"]+) "', r'"\1"'),
            (" ([" + punc_after + "])", r"\1"),  # remove space before
            ("([" + punc_before + "]) ", r"\1"),  # remove space after
            # put space after . and :
            (
                "([" + punc_after[:3] + "])([^ " + punc_after + r"\d۰۱۲۳۴۵۶۷۸۹])",
                r"\1 \2",
            ),
            (
                "([" + punc_after[3:] + "])([^ " + punc_after + "])",
                r"\1 \2",
            ),  # put space after
            (
                "([^ " + punc_before + "])([" + punc_before + "])",
                r"\1 \2",
            ),  # put space before
            # put space after number; e.g., به طول ۹متر -> به طول ۹ متر
            (r"(\d)([آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی])", r"\1 \2"),
            # put space after number; e.g., به طول۹ -> به طول ۹
            (r"([آابپتثجچحخدذرزژسشصضطظعغفقکگلمنوهی])(\d)", r"\1 \2"),
        ]

        self.affix_spacing_patterns = [
            (r"([^ ]ه) ی ", r"\1‌ی "),  # fix ی space
            (r"(^| )(ن?می) ", r"\1\2‌"),  # put zwnj after می, نمی
            # put zwnj before تر, تری, ترین, گر, گری, ها, های
            (
                r"(?<=[^\n\d "
                + punc_after
                + punc_before
                + "]{2}) (تر(ین?)?|گری?|های?)(?=[ \n"
                + punc_after
                + punc_before
                + "]|$)",
                r"‌\1",
            ),
            # join ام, ایم, اش, اند, ای, اید, ات
            (
                r"([^ ]ه) (ا(م|یم|ش|ند|ی|ید|ت))(?=[ \n" + punc_after + "]|$)",
                r"\1‌\2",
            ),
            # شنبهها => شنبه‌ها
            ("(ه)(ها)", r"\1‌\2"),
        ]

        self.specials_chars_patterns = [
            (
                "[\u0605\u0653\u0654\u0655\u0656\u0657\u0658\u0659\u065a\u065b\u065c\u065d\u065e\u065f\u0670\u0610\u0611\u0612\u0613\u0614\u0615\u0616\u0618\u0619\u061a\u061e\u06d4\u06d6\u06d7\u06d8\u06d9\u06da\u06db\u06dc\u06dd\u06de\u06df\u06e0\u06e1\u06e2\u06e3\u06e4\u06e5\u06e6\u06e7\u06e8\u06e9\u06ea\u06eb\u06ec\u06ed\u06fd\u06fe\u08ad\u08d4\u08d5\u08d6\u08d7\u08d8\u08d9\u08da\u08db\u08dc\u08dd\u08de\u08df\u08e0\u08e1\u08e2\u08e3\u08e4\u08e5\u08e6\u08e7\u08e8\u08e9\u08ea\u08eb\u08ec\u08ed\u08ee\u08ef\u08f0\u08f1\u08f2\u08f3\u08f4\u08f5\u08f6\u08f7\u08f8\u08f9\u08fa\u08fb\u08fc\u08fd\u08fe\u08ff\ufbb2\ufbb3\ufbb4\ufbb5\ufbb6\ufbb7\ufbb8\ufbb9\ufbba\ufbbb\ufbbc\ufbbd\ufbbe\ufbbf\ufbc0\ufbc1\ufc5e\ufc5f\ufc60\ufc61\ufc62\ufc63\ufcf2\ufcf3\ufcf4\ufd3e\ufd3f\ufe70\ufe71\ufe72\ufe76\ufe77\ufe78\ufe79\ufe7a\ufe7b\ufe7c\ufe7d\ufe7e\ufe7f\ufdfa\ufdfb]",
                "",
            ),
        ]

        self.replacements = [
            ("﷽", "بسم الله الرحمن الرحیم"),
            ("﷼", "ریال"),
            ("(ﷰ|ﷹ)", "صلی"),
            ("ﷲ", "الله"),
            ("ﷳ", "اکبر"),
            ("ﷴ", "محمد"),
            ("ﷵ", "صلعم"),
            ("ﷶ", "رسول"),
            ("ﷷ", "علیه"),
            ("ﷸ", "وسلم"),
            ("ﻵ|ﻶ|ﻷ|ﻸ|ﻹ|ﻺ|ﻻ|ﻼ", "لا"),
        ]

        self.tokenizer = WordTokenizer(join_verb_parts=False)
        self.verbs = Lemmatizer(joined_verb_parts=False).verbs
        self.words = self.tokenizer.words

    def normalize(self, text: str) -> str:

        translations = Normalizer.maketrans(self.translation_src, self.translation_dst)
        text = text.translate(translations)

        if self._persian_numbers:
            text = self.persian_numbers(text=text)

        if self._remove_diacritics:
            text = self.remove_diacritics(text=text)

        if self._remove_specials_chars:
            text = self.remove_specials_chars(text=text)

        if self._correct_spacing:
            text = self.correct_spacing(text=text)

        if self._unicodes_replacement:
            text = self.unicodes_replacement(text=text)

        return text

    def token_spacing(self, tokens):
        result = []
        for t, token in enumerate(tokens):
            joined = False

            if result:
                token_pair = result[-1] + "‌" + token
                if (
                    token_pair in self.verbs
                    or token_pair in self.words
                    and self.words[token_pair][0] > 0
                ):
                    joined = True

                    if (
                        t < len(tokens) - 1
                        and token + "_" + tokens[t + 1] in self.verbs
                    ):
                        joined = False

                elif token in self.suffixes and result[-1] in self.words:
                    joined = True

            if joined:
                result.pop()
                result.append(token_pair)
            else:
                result.append(token)

        return result

    def correct_spacing(self, text: str) -> str:
        text = Normalizer.regex_replace(self.extra_space_patterns, text)

        lines = text.split("\n")
        result = []
        for line in lines:
            tokens = self.tokenizer.tokenize(line)
            spaced_tokens = self.token_spacing(tokens)
            line = " ".join(spaced_tokens)
            result.append(line)

        text = "\n".join(result)

        text = Normalizer.regex_replace(self.affix_spacing_patterns, text)
        return Normalizer.regex_replace(self.punctuation_spacing_patterns, text)

    def unicodes_replacement(self, text: str) -> str:
        for old, new in self.replacements:
            text = re.sub(old, new, text)

        return text

    def remove_diacritics(self, text: str) -> str:
        return Normalizer.regex_replace(self.diacritics_patterns, text)

    def remove_specials_chars(self, text: str) -> str:
        return Normalizer.regex_replace(self.specials_chars_patterns, text)

    def persian_numbers(self, text: str) -> str:
        translations = Normalizer.maketrans(
            self.number_translation_src,
            self.number_translation_dst,
        )
        return text.translate(translations)

    @staticmethod
    def regex_replace(patterns: str, text: str) -> str:
        for pattern, repl in patterns:
            text = re.sub(pattern, repl, text)
        return text

    @staticmethod
    def maketrans(a: str, b: str):
        return {ord(a): b for a, b in zip(a, b)}