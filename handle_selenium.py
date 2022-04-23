import time

from selenium import webdriver
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec


class Currency:
    def __init__(self):
        self.download_path = {"download.default_directory": __file__.replace("handle_selenium.py", "") + "Downloads"}
        self.opt = Options()
        # self.opt.add_argument("--headless")
        self.opt.add_experimental_option("prefs", self.download_path)
        self.browser = webdriver.Chrome(executable_path='ChromeDriver/chromedriver', options=self.opt)
        self.act = ActionChains(self.browser)
        self.wait30 = WebDriverWait(self.browser, 30)
        self.wait2min = WebDriverWait(self.browser, 120)

    def get_currency_file(self, months_back):
        print('Downloading files now...')
        self.browser.get(
            'https://www.cnb.cz/cs/financni-trhy/devizovy-trh/kurzy-devizoveho-trhu/kurzy-devizoveho-trhu/vybrane_form.html')
        cookies = self.wait30.until(ec.presence_of_element_located((By.XPATH, '//*[@id="cookiebar-agree"]')))
        cookies.click()
        # self.browser.find_element(by=By.XPATH, value='//*[@id="cookiebar-agree"]')
        month = self.browser.find_element(by=By.XPATH,
                                          value='//*[@id="apollo-page"]/section/div[2]/div/div/main/div/div/div/div/div/form/div/div[1]/label[2]/select')
        month.click()
        [month.send_keys(Keys.UP) for _ in range(months_back)]
        self.act.send_keys(Keys.ENTER).perform()
        currency = self.browser.find_element(by=By.XPATH,
                                             value='//*[@id="apollo-page"]/section/div[2]/div/div/main/div/div/div/div/div/form/div/div[3]/label[2]/select')
        currency.click()
        for _ in range(14):
            currency.send_keys(Keys.DOWN)
        self.act.send_keys(Keys.ENTER).perform()
        output_format = self.browser.find_element(by=By.XPATH,
                                                  value='//*[@id="apollo-page"]/section/div[2]/div/div/main/div/div/div/div/div/form/div/div[4]/label[2]/select')
        output_format.click()
        [output_format.send_keys(Keys.DOWN) for _ in range(3)]
        self.act.send_keys(Keys.ENTER).perform()
        submit = self.browser.find_element(by=By.XPATH,
                                           value='//*[@id="apollo-page"]/section/div[2]/div/div/main/div/div/div/div/div/form/div/div[5]/button')
        submit.click()

    def get_prices_file(self, months_back):
        self.browser.get("https://www.ote-cr.cz/cs/kratkodobe-trhy/plyn/vnitrodenni-trh")
        cookies = self.wait30.until(ec.presence_of_element_located((By.XPATH, '//*[@id="optOutCookieBttnAgreeAll"]')))
        cookies.click()
        for _ in range(months_back):
            # Click on the next month button
            self.browser.find_element(by=By.XPATH,
                                      value='//*[@id="content-core"]/div/div[1]/span[1]').click()
            time.sleep(1)
        download = self.browser.find_element(By.XPATH, value='//*[@id="content-core"]/div/div[2]/div[3]/p[1]/a')
        self.act.move_to_element(to_element=download).perform()
        self.act.click().perform()
