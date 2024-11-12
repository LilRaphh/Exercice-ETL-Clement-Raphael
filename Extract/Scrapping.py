import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
import re

class Scrapping:

    def __init__(self):
        self.driver = webdriver.Chrome()
        self.link = "https://www.infoclimat.fr/observations-meteo/temps-reel/rennes-st-jacques/07130.html"

    def scrap_site(self) -> list:
        """
        Va chercher des informations sur le site infoclimat afin de récupéré les données en temps réél de la météo de rennes. 
        Récypère toutes les data de la page active. 

        Scrap:
        - Selenium

        Returns:
        - Liste des colones du tableau 
        - Liste des datas 
        """

        self.driver.get(self.link)

        tab =  self.driver.find_element(By.ID, 'resptable-releves')

        thead = tab.find_element(By.TAG_NAME, 'thead').find_element(By.TAG_NAME, 'tr').find_elements(By.TAG_NAME, 'th')

        col = [i.text for i in thead]

        col.append("Date")

        tbody = tab.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')

        data = []
        for tr in tbody:
            tbody_heur = tr.find_element(By.TAG_NAME, 'th')
            tbody_date = tbody_heur.find_element(By.TAG_NAME, 'span').get_attribute('original-title')
            date_match = re.search(r'\d{2}/\d{2}/\d{4}', tbody_date)
            if date_match:
                date = date_match.group()                
            else:
                date = ""

            data_temp = [i.text for i in tr.find_elements(By.TAG_NAME, 'td')]
            data_temp.insert(0, tbody_heur.text)
            data_temp.append(date)
            data.append(data_temp)

        time.sleep(1)
        self.driver.quit()

        return col, data
    
    def scrap_last_hour(self) -> list:
        """
        Va chercher des informations sur le site infoclimat afin de récupéré les données en temps réél de la météo de rennes. 
        Récupère les datas de la dernière heure. 

        Scrap:
        - Selenium

        Returns:
        - Liste des datas de la dernière heure
        """

        self.driver.get(self.link)
        tab =  self.driver.find_element(By.ID, 'resptable-releves')
        tbody = tab.find_element(By.TAG_NAME, 'tbody').find_element(By.TAG_NAME, 'tr')
        tbody_heur = tbody.find_element(By.TAG_NAME, 'th')
        data = [i.text for i in tbody.find_elements(By.TAG_NAME, 'td')]
        data.insert(0, tbody_heur.text)

        return data

