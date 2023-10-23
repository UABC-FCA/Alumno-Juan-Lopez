import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup


s = Service(ChromeDriverManager().install())
options = Options()
options.add_argument("--window-size= 1020, 1200")
#options.add_argument("--headless=new")

navegador = webdriver.Chrome(service=s, options=options)
navegador.get("http://www.olympedia.org/statistics/medal/country")

time.sleep(2)


cmbGender = navegador.find_element(By.NAME, "athlete_gender")
cmbYear = navegador.find_element(By.NAME,"edition_id")

genderOptions = cmbGender.find_elements(By.TAG_NAME, "option")
yearGroups = cmbYear.find_elements(By.TAG_NAME, "optgroup")

yearOptions= yearGroups[0].find_elements(By.TAG_NAME, value= "option")

d_res = {"gender":[], "year":[], "country":[], "gold":[],
         "silver":[], "bronze":[], "total":[]}


for gender in genderOptions[1:]:
    gender.click()
    #time.sleep(1)
    for year in yearOptions:
        year.click()
        time.sleep(2)

        the_soup = BeautifulSoup(navegador.page_source, 'html.parser')
        table= the_soup.find("table", attrs={"class":"table table-striped"})
        list_rows = table.find_all("tr")

        for row in list_rows[1:]:
            d_res["gender"].append(gender.text)
            d_res["year"].append(year.text)
            d_res["country"].append(row.td.text)
            medal_values = row.td.find_all_next("td", limit=5)
            d_res["gold"].append(medal_values[1].text)
            d_res["silver"].append(medal_values[2].text)
            d_res["bronze"].append(medal_values[3].text)
            d_res["total"].append(medal_values[4].text)

navegador.close()


data_df = pd.DataFrame(d_res)
data_df.to_csv("data_olimpic.csv")

