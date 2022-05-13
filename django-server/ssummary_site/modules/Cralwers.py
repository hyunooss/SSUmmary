from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

from .utils import to_sentences


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
