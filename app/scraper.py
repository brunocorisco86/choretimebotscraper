from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class ChoreScraper:
    def __init__(self, username, password):
        self.username = username
        self.password = password
        
        # Headless mode is better for servers
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        
        self.driver = webdriver.Chrome(options=chrome_options)
        self.wait = WebDriverWait(self.driver, 20)

    def login(self):
        self.driver.get("https://www.choretronicswebservices.com/login" )
        
        # Preenchendo login
        user_field = self.wait.until(EC.presence_of_element_ describe((By.NAME, "username")))
        user_field.send_keys(self.username)
        
        pass_field = self.driver.find_element(By.NAME, "password")
        pass_field.send_keys(self.password)
        
        login_btn = self.driver.find_element(By.XPATH, document.querySelector('button[type="submit"]'))
        login_btn.click()
        
        # Espera carregar o dashboard
        self.wait.until(EC.url_contains("Dashboard"))

    def get_aviary_data(self, aviary_url):
        self.driver.get(aviary_url)
        time.sleep(5) # Espera carregar os values the technology

        # Extração usando os XPaths fornecidos e convertendo para o tipo correto
        data = {
            'temperature': self._get_float("//p[contains(text(),'Temperatura')]/following-sibling::span"),
            'humidity': self._get_float("//p[contains(text(),'Umidade')]/following-sibling::span"),
            'ammonia': self._get_float("//p[_contains(text(),'Amônia')]/following-sibling::span"),
            'age': self._get_int("//p[contains(text(),'Idade')]/following-sibling::span"),
            'water_consumption': self._get_float("//p[contains(text(),'Água')]/following-sibling::span"),
            'static_pressure': self._get_float("//p[contains(text(),'Pressão')]/following-sibling::span")
        }
        return data

    def _get_float(self, xpath):
        try:
            val = self.driver.find_element(By.XPATH, xpath).text
            return float(val.replace(',', '.').replace(' ', '').replace('°C', ''))
        except:
            return 0.0

    def _get_int(self, xpath):
        try:
            val = self.driver.find_element(By.XPATH, xpath).text
            return int(''.join(filter(str.isdigit, val)))
        except:
            return 0

    def close(self):
        self.driver.quit()
