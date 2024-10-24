import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.common.by import By

class Scrapping:

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.link = "https://www.infoclimat.fr/observations-meteo/temps-reel/rennes-st-jacques/07130.html"

    def scrap_site(self) -> list:
        self.driver.get(self.link)

        tab =  self.driver.find_element(By.ID, 'resptable-releves')

        thead = tab.find_element(By.TAG_NAME, 'thead').find_element(By.TAG_NAME, 'tr').find_elements(By.TAG_NAME, 'th')

        col = [i.text for i in thead]

        tbody = tab.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')

        data = []
        for tr in tbody:
            tbody_heur = tr.find_element(By.TAG_NAME, 'th')
            data_temp = [i.text for i in tr.find_elements(By.TAG_NAME, 'td')]
            data_temp.insert(0, tbody_heur.text)
            data.append(data_temp)

        time.sleep(1)
        self.driver.quit()

        return col, data
    
    def scrap_last_hour(self) -> list:
        self.driver.get(self.link)
        tab =  self.driver.find_element(By.ID, 'resptable-releves')
        tbody = tab.find_element(By.TAG_NAME, 'tbody').find_element(By.TAG_NAME, 'tr')
        tbody_heur = tbody.find_element(By.TAG_NAME, 'th')
        data = [i.text for i in tbody.find_elements(By.TAG_NAME, 'td')]
        data.insert(0, tbody_heur.text)

        return data

