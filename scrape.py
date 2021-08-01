import logging
import requests
from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.common.exceptions import TimeoutException,WebDriverException

from random_user_agent.user_agent import UserAgent
from random_user_agent.params import SoftwareName,OperatingSystem

from time import sleep

class Request:
    
    logger = logging.getLogger('Selenium intensifies')
    selenium_retries = 0

    def __init__(self, url):
        self.url = url

    def get_selenium_res(self,class_name):
        try:
            software_names = [SoftwareName.CHROME.value]
            operating_systems = [OperatingSystem.WINDOWS.value, OperatingSystem.LINUX.value]

            user_agent_rotator = UserAgent(software_names=software_names, operating_systems=operating_systems, limit=100)

            user_agent = user_agent_rotator.get_random_user_agent()
            chrome_options = Options()
            chrome_options.add_argument(f'user-agent:{user_agent}')
            chrome_options.add_argument('--disable-gpu')
            chrome_options.add_argument('--headless')
            chrome_options.add_argument('--no-sandbox')

            PROXY = "https://95.156.230.45:80"

            if not IS_GAE_PRODUCTION_ENV:
                chrome_options.binary_location = '/etc/alternatives/google-chrome'
            prox = Proxy()
            prox.auto_detect = False
            prox.proxy_type = ProxyType.MANUAL
            capabilities = webdriver.DesiredCapabilities.CHROME
            prox.http_proxy = PROXY
            prox.ssl_proxy = PROXY
            prox.add_to_capabilities(capabilities)

            browser = webdriver.Chrome(chrome_options=chrome_options)
            # browser.get(self.url)
            browser.get('http://lumtest.com/myip.json')

        except (TimeoutException, WebDriverException):
            self.logger.error(traceback.format_exc())
            sleep(6)
            self.selenium_retries += 1
            self.logger.info('Selenium retyr # '+ str(self.selenium_retries))
            return self.get_selenium_res(class_name)

req = Request(None)
req.get_selenium_res(None)