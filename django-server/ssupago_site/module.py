from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class Converter():
    def __init__(self):
        path = ChromeDriverManager().install()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--log-level=3")
        options.add_experimental_option('useAutomationExtension', False)
        self.browser = webdriver.Chrome(path, options=options)

    def trans_with_papago(self, text):
        url = "https://papago.naver.com/?sk=auto&tk=ko&st="
        # preprocessing
        text = text.replace('{', '%7B')
        text = text.replace('}', '%7D')
        text = text.replace('[', '%5B')
        text = text.replace(']', '%5D')
        text = text.replace('^', '%5E')

        # retrial
        for trial in range(3):
            try:
                self.browser.get(url + text)
                result = WebDriverWait(self.browser, 30).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="txtTarget"]/span'))
                ).text
            except Exception as e:
                if trial == 2:
                    print(url + text)
                    raise e
            else:
                break
        return result

    def summ_with_sumz3(self, text):
        url = "https://summariz3.herokuapp.com/"

        # retrial
        for trial in range(3):
            try:
                self.browser.get(url)
                
                # '요약하고 싶은 텍스트' 입력
                textArea = WebDriverWait(self.browser, 30).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="input-3"]'))
                )
                textArea.send_keys(text)
                
                # '요약하기' 버튼
                btn = WebDriverWait(self.browser, 30).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="container"]/form/div[2]/button'))
                )
                btn.click()
                
                # '요약 결과'
                result = WebDriverWait(self.browser, 60).until(
                    EC.presence_of_element_located((By.XPATH, '//*[@id="container"]/div[2]/div[2]'))
                ).text
            except Exception as e:
                if trial == 2:
                    raise e
            else:
                break
        return result
