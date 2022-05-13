from selenium import webdriver
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MyCralwer:
    def __init__(self):
        # initialize browser
        path = ChromeDriverManager().install()
        options = webdriver.ChromeOptions()
        options.add_argument("--headless")
        options.add_argument("--log-level=3")
        options.add_experimental_option('useAutomationExtension', False)
        self.browser = webdriver.Chrome(path, options=options)
        print("Log: browser loaded successfully")
