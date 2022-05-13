import urllib.request

from langdetect import detect
from googletrans import Translator

from .utils import divide


class Translater_with_papago_api:
    def __init__(self):
        self.client_id = "ACTEz0YaXKIVplDTV2lE"
        self.client_secret = "PnDLJZHsZl"

    def translate(self, text):
        result = None

        lang = detect(text)
        encText = urllib.parse.quote(text)
        data = f"source={lang}&target=en&text=" + encText
        url = "https://openapi.naver.com/v1/papago/n2mt"

        request = urllib.request.Request(url)
        request.add_header("X-Naver-Client-Id", self.client_id)
        request.add_header("X-Naver-Client-Secret", self.client_secret)
        response = urllib.request.urlopen(request, data=data.encode("utf-8"))
        
        rescode = response.getcode()
        if rescode == 200:
            response_body = response.read()
            result = response_body.decode('utf-8')
        else:
            result = "Error Code:" + rescode

        return result

    def translate(self, text, input_size=5000):
        return self.translate(text)

class Translater_with_googletrans:
    def __init__(self):
        self.translator = Translator()

    def translate(self, text, input_size=5000):
        # do not translate if text is Korean.
        if detect(text) == 'ko':
            return text

        result = ""
        dumps = divide(text, input_size=input_size)
        for dump in dumps:
            result += self.translator.translate(dump, dest='ko').text
        return result
