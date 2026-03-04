from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
import logging

class ChoreScraper:
    def __init__(self, user, password):
        chrome_options = Options()
        chrome_options.add_argument("--headless")
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        self.driver = webdriver.Chrome(options=chrome_options)
        self.user = user
        self.password = password
        self.wait = WebDriverWait(self.driver, 20)

    def login(self):
        try:
            self.driver.get("https://www.choretronicswebservices.com/" )
            self.wait.until(EC.presence_of_element_located((By.NAME, "username"))).send_keys(self.user)
            self.driver.find_element(By.NAME, "password").send_keys(self.password)
            self.driver.find_element(By.CSS_SELECTOR, "button[type='submit']").click()
            self.wait.until(EC.url_contains("/connect/"))
            return True
        except: return False

    def scrape_aviary(self, url):
        self.driver.get(url)
        time.sleep(10)
        data = {}
        try:
            # XPaths fornecidos pelo usuário
            data['temperature'] = self._get_val("/html/body/div[1]/main/article/div[1]/div/div[1]/div/div[1]/div/div[1]/button/span/div/div/text()[1]")
            data['humidity'] = self._get_val("/html/body/div[1]/main/article/div[1]/div/div[1]/div/div[2]/div[2]/div/div[5]/span")
            data['ammonia'] = self._get_val("/html/body/div[1]/main/article/div[1]/div/div[1]/div/div[2]/div[2]/div/div[14]/span/text()")
            data['age'] = int(self._get_val("/html/body/div[2]/span[2]/text()[3]").split()[0])
            data['water_consumption'] = self._get_val("/html/body/div[1]/main/article/div[1]/div/div[1]/div/div[1]/div/div[2]/button/span/div/div/text()[1]")
            data['static_pressure'] = self._get_val("/html/body/div[1]/main/article/div[1]/div/div[1]/div/div[2]/div[2]/div/div[2]/span")
            return data
        except: return None

    def _get_val(self, xpath):
        try:
            script = f"return document.evaluate(\"{xpath}\", document, null, XPathResult.STRING_TYPE, null).stringValue;"
            res = self.driver.execute_script(script) or self.driver.find_element(By.XPATH, xpath).text
            return res.strip().replace(',', '.')
        except: return "0"

    def close(self): self.driver.quit()
