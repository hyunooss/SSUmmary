from .Translaters import *
from .Summarizers import *

from hanspell import spell_checker


class MyConverter:
    def __init__(self):
        # initialize translater instance
        self.translater = Translater_with_googletrans()
        # self.translater = Translater_with_papago_api()
        print("=" * 50)
        print("Log: translater 초기화 성공")       

        # initialize summarizer instance
        # self.summarizer = Summarizer_with_KoBart('digit82/kobart-summarization')
        # self.summarizer = Summarizer_with_Bart_r3f('alaggung/bart-r3f')
        self.summarizer = Summarizer_with_textrank()
        print("Log: summarizor 초기화 성공")
        print("=" * 50, end="\n\n")

    def translate(self, text, target, input_size=5000):
        """
        Translate the text into Korean by dividing it into chunks.

        Args:
            text (str): Text to be translated
            target (str): Target language
            input_size (int): Size of each chunk
        """
        return self.translater.translate(text, target, input_size=input_size)

    def spell_check(self, text, input_size=500):
        """
        Check the spelling of the text.

        Args:
            text (str): Text to be checked
            input_size (int): Size of each chunk
        """

        result = ""
        dumps = divide(text, input_size=input_size)

        for dump in dumps:
            result += spell_checker.check(dump).checked
        return result

    def summarize(self, text, input_size=1024, deep=False):
        """
        Summarize the text by dividing it into chunks.

        args:
            text (str): Text to be translated
            input_size (int): Size of each chunk
            deep (bool): Whether to use deep summarization
        """
        return self.summarizer.generate(text, input_size=input_size, deep=deep)
