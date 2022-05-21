from .Cralwers import *

import fasttext.util
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import networkx as nx

import torch
from transformers import PreTrainedTokenizerFast
from transformers import BartForConditionalGeneration

from .utils import *


class Summarizer_with_Cralwing:
    def __init__(self):
        self.url = "https://summariz3.herokuapp.com"
        self.browser = MyCralwer().browser

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

class Summarizer_with_textrank:
    # 추출 요약 기반 텍스트 랭크
    def __init__(self):
        fasttext.FastText.eprint = lambda x: None
        self.ft = fasttext.load_model('models/cc.ko.300.bin')
        
    def similarity_matrix(self, sentence_embedding):
        embedding_dim = 300
        sim_mat = np.zeros([len(sentence_embedding), len(sentence_embedding)])
        for i in range(len(sentence_embedding)):
            for j in range(len(sentence_embedding)):
                sim_mat[i][j] = cosine_similarity(sentence_embedding[i].reshape(1, embedding_dim),
                                            sentence_embedding[j].reshape(1, embedding_dim))[0,0]
        return sim_mat    
        
    def calculate_sentence_vector(self, sentence):
        embedding_dim = 300
        zero_vector = np.zeros(embedding_dim)
        if len(sentence) == 0:
            return zero_vector
        return sum([self.ft.get_word_vector(word) for word in sentence])/len(sentence)
    
    def calculate_score(self, sim_matrix):
        nx_graph = nx.from_numpy_array(sim_matrix)
        scores = nx.pagerank(nx_graph)
        return scores
    
    def ranked_sentences(self, sentences, scores, n=3):
        top_scores = sorted(((scores[i],s) for i,s in enumerate(sentences)), reverse=True)
        top_n_sentences = [sentence for score,sentence in top_scores[:n]]
        return "".join(top_n_sentences)
        
    def generate(self, text, input_size=1024, deep=False):
        n = 1 if deep else 3
        
        sentences = [s + '.' for s in text.split('.')]
        
        sentence_vectors = [self.calculate_sentence_vector(sentence) for sentence in sentences]
        matrixs = self.similarity_matrix(sentence_vectors)
        scores = self.calculate_score(matrixs)
        
        return self.ranked_sentences(sentences, scores, n)
        
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

class Summarizer_with_Bart_r3f:
    def __init__(self, model_name):
        self.tokenizer = PreTrainedTokenizerFast.from_pretrained(model_name)
        self.model     = BartForConditionalGeneration.from_pretrained(model_name)
        
    def generate(self, text, input_size=512, deep=False):
        if input_size > 512:
            raise ValueError("input_size must be less than 512")

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
            
            for i in range(0, len(text), input_size):
                dump = text[i:i+input_size]
                dump = " ".join(dump.split()).split(".")
                dump = [s for s in dump if s != ""]

                raw_input_ids = self.tokenizer("[BOS]" + "[SEP]".join(dump) + "[EOS]", return_tensors="pt")

                outputs = self.model.generate(
                    raw_input_ids.input_ids,
                    attention_mask=raw_input_ids.attention_mask,
                    num_beams=5,
                    length_penalty=1.2,
                    max_length=512,
                    use_cache=True,
                )
                result += self.tokenizer.decode(outputs[0], skip_special_tokens=True)
        return result
