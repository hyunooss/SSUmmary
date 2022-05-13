from .Cralwers import *

import urllib.request

from langdetect import detect
from googletrans import Translator

from .utils import *


class Translater_with_Cralwing:
    def __init__(self):
        self.browser = MyCralwer().browser

    def translate(self, text, target):
        url = f"https://papago.naver.com/?sk=auto&tk={target}&st="

        # preprocessing
        text = text.replace('%', '%25')
        text = text.replace('{', '%7B')
        text = text.replace('}', '%7D')
        text = text.replace('[', '%5B')
        text = text.replace(']', '%5D')
        text = text.replace('^', '%5E')
        text = text.replace('`', '%60')
        text = text.replace('\\', '%5C')
        text = text.replace('|', '%7C')

        # text to sentence
        sentences = to_sentences(text)

        # translate each sentence
        result, dumps = "", ""
        for i in range(len(sentences)):
            dumps += sentences[i] + "."

            if len(dumps) >= 800 or i == len(sentences)-1:
                # retry 3 times
                for trial in range(3):
                    try:
                        self.browser.get(url + dumps)
                        result += WebDriverWait(self.browser, 30).until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="txtTarget"]/span'))
                        ).text

                        # clean dumps
                        dumps = ""
                    except Exception as e:
                        if trial == 2:
                            print(url + dumps)
                            raise e
                    else:
                        break
        return result

    def translate(self, text, target, input_size=5000):
        return self.translate(text, target)

class Translater_with_papago_api:
    def __init__(self):
        self.client_id = "ACTEz0YaXKIVplDTV2lE"
        self.client_secret = "PnDLJZHsZl"

    def translate(self, text, target):
        result = None

        lang = detect(text)
        encText = urllib.parse.quote(text)
        data = f"source={lang}&target={target}&text=" + encText
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

    def translate(self, text, target, input_size=5000):
        return self.translate(text, target)

class Translater_with_googletrans:
    def __init__(self):
        self.translator = Translator()

    def translate(self, text, target, input_size=5000):
        # do not translate if text is Korean.
        if detect(text) == target:
            return text

        result = ""
        dumps = divide(text, input_size=input_size)
        for dump in dumps:
            result += self.translator.translate(dump, dest=target).text
        return result
