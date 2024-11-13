import random
import pandas as pd
from selenium import webdriver
import time
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import re
from datetime import datetime, timedelta
import locale

class Scrapping:


    def __init__(self):

        locale.setlocale(locale.LC_TIME, 'fr_FR.UTF-8')
    
        self.link = "https://www.infoclimat.fr/observations-meteo/temps-reel/rennes-st-jacques/07130.html"
        self.USER_AGENTS = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36 Edge/91.0.864.67",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_6) AppleWebKit/537.36 (KHTML, like Gecko) Firefox/89.0",
            "Mozilla/5.0 (Windows NT 6.1; WOW64; rv:51.0) Gecko/20100101 Firefox/51.0",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:91.0) Gecko/20100101 Firefox/91.0",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36",
            "Mozilla/5.0 (Windows NT 6.1; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/86.0.4240.111 Safari/537.36",
            "Mozilla/5.0 (Linux; Android 9; SM-G960F) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.115 Mobile Safari/537.36",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.114 Safari/537.36"
        ]

    # Fonction pour initialiser le driver avec un User-Agent donné
    def create_driver_with_user_agent(user_agent):

        """
        Configuration du driver chrome pour optimiser les performances
        Permet de changer de user_agent afin de bypass les captcha 

        Args:
        - user_agent -> Une liste de user_agent

        Return:
        - driver -> le driver de configuration de notre scraper
        """
        chrome_options = Options()
        chrome_options.add_argument(f"user-agent={user_agent}")
        chrome_options.add_argument("--headless")  # Pour exécuter sans fenêtre
        chrome_options.add_argument("--no-sandbox")
        chrome_options.add_argument("--disable-dev-shm-usage")
        chrome_options.add_argument("--window-size=1920,1080")
        
        # Crée le driver avec les options
        driver = webdriver.Chrome(options=chrome_options)
        return driver

    def get_date(date_start) -> list:
        """
        Recupère une liste de date à partir d'une date de début jusqu'a aujourd'hui

        Args:
        - date_start -> Date de début 

        Returns:
        - dates -> liste de date 
        """

        date = datetime.now()
        date_start = datetime.strptime(date_start, "%Y-%m-%d %H:%M:%S")

        dates = []

        while date_start < date - timedelta(days=1):
            dates.append(date_start)
            date_start += timedelta(days=1)

        return dates

    def scrap_with_start_date(self, date_start):
        """
        /!\ Processus long en fonction du nombre de date à parcourir /!\ 

        Permet de récupérer toutes les données du sites à partir d'une date de début jusqu'à aujourd'hui
        
        Args:
        - date_start (format: 2023-01-01 00:00:00) -> date de debut du processus de scraping 

        Return:
        - créer un csv avec toutes les données scrap
        - df -> Retourne le dataframe avec les données scrap 
        
        """


        # Liste pour stocker les données
        data = []

        dates = self.get_date(date_start)

        # Pour chaque lien, essayez différents User-Agent en cas d'échec
        for date in dates:

            jour = date.day
            mois = date.strftime('%B').replace('Ã©', 'e').replace('Ã»', 'u')
            annee = date.year

            if jour == 1:
                jour = '1er'

            # user_agent = random.choice(USER_AGENTS)  # Choisir un User-Agent au hasard
            driver = self.create_driver_with_user_agent(self.USER_AGENTS)

            # Essayer plusieurs fois avec différents User-Agent si le tableau n'est pas trouvé
            retries = 3
            for attempt in range(retries):
                try:
                    driver.get(f"https://www.infoclimat.fr/observations-meteo/archives/{jour}/{mois}/{annee}/rennes-st-jacques/07130.html",)
                    
                    WebDriverWait(driver, 10).until(EC.visibility_of_element_located((By.ID, "resptable-releves")))

                    
                    # Essayer de trouver le tableau
                    tab = driver.find_element(By.ID, 'resptable-releves')
                    thead = tab.find_element(By.TAG_NAME, 'thead').find_element(By.TAG_NAME, 'tr').find_elements(By.TAG_NAME, 'th')
                    col = [i.text for i in thead]
                    tbody = tab.find_element(By.TAG_NAME, 'tbody').find_elements(By.TAG_NAME, 'tr')

                    # Ajouter les données à la liste
                    for tr in tbody:
                        tbody_heur = tr.find_element(By.TAG_NAME, 'th')
                        tbody_date = tbody_heur.find_element(By.TAG_NAME, 'span').get_attribute('original-title')
                        date_match = re.search(r'\d{2}/\d{2}/\d{4}', tbody_date)
                        if date_match:
                            date_jour = date_match.group()                
                        else:
                            date_jour = ""
                            
                        try:
                            # Format : dd/mm/yyyy hh
                            date_time = datetime.strptime(f"{date_jour} {tbody_heur.text.replace('h', '')}", "%d/%m/%Y %H")
                        except ValueError:
                            date_time = None  # Gérer les erreurs de conversion en datetime

                        data_temp = [i.text for i in tr.find_elements(By.TAG_NAME, 'td')]
                        data_temp.insert(0, date_time)
                        data.append(data_temp)

                    print(f"La page du {jour} {mois} {annee} a été scrap !")
                    break  # Sortir de la boucle en cas de succès

                except Exception as e:
                    if attempt == retries - 1:
                        print("Échec après plusieurs tentatives, passer au lien suivant.")
                    else:
                        # Choisir un autre User-Agent pour la prochaine tentative
                        user_agent = random.choice(self.USER_AGENTS)
                        driver.quit()
                        driver = self.create_driver_with_user_agent(user_agent)
        
        df = pd.DataFrame(data, columns=col)

        df.to_csv(f'../dataset/meteo_rennes_start_{dates[0].strftime("%d-%m-%Y")}.csv')

        return df

    def scrap_site(self) -> list:
        """
        Va chercher des informations sur le site infoclimat afin de récupéré les données en temps réél de la météo de rennes. 
        Récypère toutes les data de la page active. 

        Scrap:
        - Selenium

        Returns:
        - col -> Liste des colones du tableau 
        - data -> Liste des datas 
        """
        
        driver = self.create_driver_with_user_agent(self.USER_AGENTS)

        driver.get(self.link)

        tab =  self.driver.find_element(By.ID, 'resptable-releves')

        thead = tab.find_element(By.TAG_NAME, 'thead').find_element(By.TAG_NAME, 'tr').find_elements(By.TAG_NAME, 'th')

        col = [i.text for i in thead]

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

            try:
                # Format : dd/mm/yyyy hh
                date_time = datetime.strptime(f"{date} {tbody_heur.text.replace('h', '')}", "%d/%m/%Y %H")
            except ValueError:
                date_time = None  # Gérer les erreurs de conversion en datetime

            data_temp = [i.text for i in tr.find_elements(By.TAG_NAME, 'td')]
            data_temp.insert(0, date_time)
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
        - data -> Liste des datas de la dernière heure
        """

        driver = self.create_driver_with_user_agent(self.USER_AGENTS)

        driver.get(self.link)
        tab =  self.driver.find_element(By.ID, 'resptable-releves')
        tbody = tab.find_element(By.TAG_NAME, 'tbody').find_element(By.TAG_NAME, 'tr')
        tbody_heur = tbody.find_element(By.TAG_NAME, 'th')
        data = [i.text for i in tbody.find_elements(By.TAG_NAME, 'td')]
        data.insert(0, tbody_heur.text)

        return data

