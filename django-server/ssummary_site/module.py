from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

import torch
from transformers import PreTrainedTokenizerFast
from transformers import BartForConditionalGeneration

import urllib.request

from langdetect import detect

from googletrans import Translator

import fasttext.util
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx


def to_sentences(text):
    text = text.replace("\n", "")
    sentences = " ".join(text.split()).split(".")
    sentences = [s for s in sentences if s != ""]
    return sentences

def divide(text, input_size=5000):
    """
    Divide text into chunks of input_size

    Args:
        text (str): Text to be divided
        input_size (int): Size of each chunk
    """
    # short input_size if asian
    lang = detect(text)
    if lang in ['ko', 'ja', 'zh-cn', 'zh-tw', 'zh-hk']:
        input_size = 1300

    # divide text by words
    text = to_sentences(text)
    result = []
    temp = ""
    for word in text:
        if len(temp + word) >= input_size:
            result.append(temp)
            temp = ""
        temp += word + " "
    result.append(temp)
    return result


class Cralwer:
    def __init__(self):
        # initialize browser
        path = ChromeDriverManager().install()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--log-level=3")
        options.add_experimental_option('useAutomationExtension', False)
        self.browser = webdriver.Chrome(path, options=options)
        print("Log: browser loaded successfully")


class Translater_with_Cralwing:
    def __init__(self):
        self.url = "https://papago.naver.com/?sk=auto&tk=ko&st="
        self.browser = Cralwer().browser

    def translate(self, text):
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

    def translate(self, text, input_size=5000):
        return self.translate(text)

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
        result = ""
        dumps = divide(text, input_size=input_size)
        for dump in dumps:
            result += self.translator.translate(dump, dest='ko').text
        return result

class Summarizer_with_Cralwing:
    def __init__(self):
        self.url = "https://summariz3.herokuapp.com"
        self.browser = Cralwer().browser

    def generate(self, text):
        # text to sentence
        sentences = to_sentences(text)

        # summarize each sentence
        result, dumps = "", ""
        for i in range(len(sentences)):
            dumps += sentences[i] + "."

            # do 40 sentences each 
            if (i+1) % 40 == 0 or i == len(sentences)-1:
                # retry 3 times
                for trial in range(3):
                    try:
                        self.browser.get(url)
                        
                        # '요약하고 싶은 텍스트' 입력
                        textArea = WebDriverWait(self.browser, 30).until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="input-3"]'))
                        )
                        self.browser.execute_script("""
                            var elm = arguments[0]; 
                            elm.value = arguments[1]; 
                            elm.dispatchEvent(new Event('change'));
                            """, textArea, dumps)
                        
                        # '요약하기' 버튼
                        btn = WebDriverWait(self.browser, 30).until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="container"]/form/div[2]/button'))
                        )
                        btn.click()
                        
                        # '요약 결과'
                        result += WebDriverWait(self.browser, 60).until(
                            EC.presence_of_element_located((By.XPATH, '//*[@id="container"]/div[2]/div[2]'))
                        ).text

                        # clean dumps
                        dumps = ""
                    except Exception as e:
                        if trial == 2:
                            print(f"{len(dumps)} \n{dumps}")
                            raise e
                    else:
                        break
        return result

    def generate(self, text, input_size=1024, deep=False):
        return self.generate(text)

class Summarizer_with_KoBart:
    def __init__(self, model_name):
        self.tokenizer = PreTrainedTokenizerFast.from_pretrained(model_name)
        self.model     = BartForConditionalGeneration.from_pretrained(model_name)
        
    def generate(self, text, input_size=1024, deep=False):
        result = ""
        
        loop = 1
        if deep == True:
            loop = 0
            size = len(text)
            while size // 100 > 0:
                size =  size // 100
                loop += 1
        
        for _ in range(loop):
            if result:
                text = result
            text = text.replace('\n', ' ')
            raw_input_ids = self.tokenizer.encode(text)

            result = ""
            for i in range(0, len(raw_input_ids), input_size):
                dump = raw_input_ids[i:i+input_size]

                input_ids = [self.tokenizer.bos_token_id] + dump + [self.tokenizer.eos_token_id]
                summary_ids = self.model.generate(torch.tensor([input_ids]),  num_beams=4,  max_length=512,  eos_token_id=1)
                result += self.tokenizer.decode(summary_ids.squeeze().tolist(), skip_special_tokens=True)
        return result

class Summarizer_with_textrank:
    def __init__(self):
        self.ft = fasttext.load_model('models/cc.ko.300.vec')
        
    def similarity_matrix(sentence_embedding):
        embedding_dim = 300
        sim_mat = np.zeros([len(sentence_embedding), len(sentence_embedding)])
        for i in range(len(sentence_embedding)):
            for j in range(len(sentence_embedding)):
                sim_mat[i][j] = cosine_similarity(sentence_embedding[i].reshape(1, embedding_dim),
                                            sentence_embedding[j].reshape(1, embedding_dim))[0,0]
        return sim_mat    
        
    def calculate_sentence_vector(sentence):
        embedding_dim = 300
        zero_vector = np.zeros(embedding_dim)
        if len(sentence) == 0:
            return zero_vector
        return sum([self.ft.get_word_vector(word) for word in sentence])/len(sentence)
    
    def calculate_score(sim_matrix):
        nx_graph = nx.from_numpy_array(sim_matrix)
        scores = nx.pagerank(nx_graph)
        return scores
    
    def ranked_sentences(sentences, scores, n=3):
        top_scores = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)
        top_n_sentences = [sentence for score,sentence in top_scores[:n]]
        return " ".join(top_n_sentences)
        
    def generate(self, text, input_size=1024, deep=False):
        result = ""
        
        loop = 1
        if deep == True:
            loop = 0
            size = len(text)
            while size // 100 > 0:
                size =  size // 100
                loop += 1
        
        for _ in range(loop):
            if result:
                text = result
            sentences = text.split('.')
            
            sentence_vectors = [self.calculate_sentence_vector(sentence) for sentence in sentences]
            matrixs = self.similarity_matrix(sentence_vectors)
            scores = self.calculate_score(matrixs)
            result = self.ranked_sentences(sentences, scores, n=3)
        
        return result
        
    
    
    

class Converter:
    def __init__(self):
        # initialize translater instance
        self.translater = Translater_with_googletrans()
        print("Log: translater loaded successfully")       

        # initialize summarizer instance
        # self.summarizer = Summarizer_with_KoBart('digit82/kobart-summarization')
        self.summarizer = Summarizer_with_textrank()
        print("Log: summarizor loaded successfully")

    def translate(self, text, input_size=5000):
        """
        Translate the text into Korean by dividing it into chunks.

        Args:
            text (str): Text to be translated
            input_size (int): Size of each chunk
        """
        return self.translater.translate(text, input_size=input_size)

    def summarize(self, text, input_size=1024, deep=False):
        """
        Summarize the text by dividing it into chunks.

        args:
            text (str): Text to be translated
            input_size (int): Size of each chunk
            deep (bool): Whether to use deep summarization
        """
        return self.summarizer.generate(text, input_size=input_size, deep=deep)
