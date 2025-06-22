import pandas as pd
import numpy as np
import time
import warnings
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import re

warnings.filterwarnings("ignore")

# chromedriver yolu
path = "C:\\Program Files (x86)\\chromedriver.exe"
service = Service(path)
driver = webdriver.Chrome(service=service)

driver.get("https://sozluk.gov.tr/")

wait = WebDriverWait(driver, 20)
    
# sözlük seç'e tıkla
select_dictionary = wait.until(EC.element_to_be_clickable((By.ID, 'tdk-srch-current-dataset')))
select_dictionary.click()
# atasözü ve deyimleri ekle
ads = wait.until(EC.element_to_be_clickable((By.ID, 'ads')))
ads.click()

# metni temizleme fonksiyonu
def clean_text(text):
    text = re.sub(r'\([^)]*\)', '', text)  # parantez içindekileri kaldırma
    text = re.sub(r'[^\w\sığüşöçİĞÜŞÖÇ]', '', text)  # özel karakterleri kaldırma
    text = text.strip()  # metnin başındaki ve sonundaki boşlukları kaldırma  
    return text

#tüm verileri saklayacağımız küme(aynı olan verileri yazdırmaması için set kullandık)
unique_data_atasözü = set()
unique_data_deyim = set()

# karakterleri yazarak veri çekmek için fonksiyon
def search(character):
    # arama butonuna harfi ekle
    search_input = wait.until(EC.presence_of_element_located((By.ID, 'tdk-srch-input')))
    search_input.clear()
    search_input.send_keys(character)

    # arama butonuna tıkla
    search_button = wait.until(EC.element_to_be_clickable((By.ID, 'tdk-search-btn')))
    search_button.click()

    max_id_reached = False
    i = 1
    # verileri getir
    while not max_id_reached and i <= 100:  
        id = "bulunan-ads" + str(i)
        special_id = "ozellikler-ads" + str(i)
        try:
            element = wait.until(EC.presence_of_element_located((By.ID, id)))
            special = wait.until(EC.presence_of_element_located((By.ID, special_id)))
            if(special.text == "Atasözü"):
                cleaned_text = clean_text(element.text)
                text_length = len(cleaned_text.replace(" ", ""))
                formatted_text = f'{cleaned_text},{text_length}'
                unique_data_atasözü.add(formatted_text)
            elif(special.text == "Deyim"):
                cleaned_text = clean_text(element.text)
                text_length = len(cleaned_text.replace(" ", ""))
                formatted_text = f'{cleaned_text},{text_length}'
                unique_data_deyim.add(formatted_text)                    
            i += 1
        except TimeoutException:
            print(f"{id} ID'li öğe bulunamadı.")
            max_id_reached = True

#aratmak istediğim harfler
characters = [" a", " b", " c", " d", " e", " f", " g", " h", " ı", " i", " k", " l", " m", " n", " o", " ö", " p", " r", " s", " ş", " t", " u", " ü", " v", " y", " z"]
#her harf için fonksiyonu çağırıp verileri çekiyorum
for char in characters:
    search(char)

def write_csv(csv_name,list_name):
    with open(csv_name, 'w', encoding='utf-8') as f:
        for line in list_name:
            f.write(line + '\n')

write_csv('atasözü.csv',unique_data_atasözü)
write_csv('deyim.csv',unique_data_deyim)
# Tarayıcıyı kapat
driver.quit()