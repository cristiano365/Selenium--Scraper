import os
import time

import wget
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait

import sys


DRIVEPATH = "C://Users//Sony//PycharmProjects//igScraper//chromedriver_win32//chromedriver.exe"
URL = "https://www.instagram.com/"
key_username = sys.argv[1]
key_pssw = sys.argv[2]
tag = sys.argv[3]


name_username = "username"
name_password = "password"
class_cookie = "aOOlW.bIiDR"
class_log = "sqdOP.L3NKy.y3zKF"
class_NonOra = "sqdOP.yWX7d.y3zKF"
class_notifiche = "aOOlW.HoLwm"




#TROVA L'ELEMENTO TRAMITE TAG CLASS_NAME
def class_search(driver,class_name):
    try:
        obj  = WebDriverWait(driver, 8).until(
            EC.presence_of_element_located((By.CLASS_NAME, class_name))
        )

    finally:
        time.sleep(5)

    return obj



##TROVA L'ELEMENTO TRAMITE IL TAG NAME
def name_search(driver,class_name):
    try:
        name = WebDriverWait(driver, 8).until(
            EC.presence_of_element_located((By.NAME, class_name))
        )

    finally:
        time.sleep(5)

    return name



#UNZIONE CHE DOPO AVER ASSOCIATO AD UNA VARIABILE IL CONTENUTO DEL TAG HTML TRAMITE IL SUO NOME
#EFFETTUA COME ESECUZIONE L'INVIO DI UNA CHIAVE DI VALORI IN CORRISPONDENZA DELL'OGGETTO SULLA PAGINA WEB
def selector_keys(driver,class_name,key):
    try:
        name = name_search(driver,class_name)
        name.send_keys(key)

    finally:
        time.sleep(5)



#FUNZIONE CHE DOPO AVER ASSOCIATO AD UNA VARIABILE IL CONTENUTO DEL TAG HTML TRAMITE IL NOME DELLA CLASSE
#EFFETTUA COME ESECUZIONE UN CLICK IN CORRISPONDENZA DELL'OGGETTO SULLA PAGINA WEB
def selector_click(driver,class_name):
    try:
      clk =  class_search(driver,class_name)
      clk.click()

    finally:
        time.sleep(5)



#FUNZIONE COMPOSTA CHE TROVA L'ELEMENTO TRAMITE IL NOME DELLA CLASSE, LO POPOLA TRAMITE L'INSERIMENTO DI UNA CHIAVE DI VALORI
#E, RICHIAMANDO LA FUNZIONE GO EFFETTUA COME ESECUZIONE LA SIMULAZIONE DELLA DIGITAZIONE DEL TASTO INVIO
def keyGo(driver,class_name,tag_name):
    try:
        search = class_search(driver,class_name)
        search.send_keys(tag_name)
        count=0
        while count <= 2:
            go(search)
            count = count + 1

    finally:
        time.sleep(8)



def go(obj):
    obj.send_keys(Keys.ENTER)
    time.sleep(8)



#SCORRE LA FINESTRA DEI POST E LI SCARICA IN UNA DIRECTORY CON LO STESSO NOME
def scrape(driver):
    driver.execute_script("window.scrollTo(0,document.body.scrollHeight);")

    posts = driver.find_elements_by_tag_name('img')
    posts = [image.get_attribute('src') for image in posts]
    posts = posts[:-2]

    path = os.getcwd()
    path = os.path.join(path, "C://Users//Sony//PycharmProjects//igScraper//" + tag)
    os.mkdir(path)

    counter = 0
    for post  in posts:
        save_as = os.path.join(path,  str(counter) + '.jpg')
        wget.download(post,save_as)
        counter += 1



#ARRIVATI ALLA HOME DI INSTAGRAM, TRAMITE LA FUNZIONE "ig_panel" SI VA AD ANALIZZARE IL #tag E PREPARA IL BOT ALLO SCRAPING
def ig_panel(driver):
    class_search = "eyXLr.wUAXj"
    button_class_search = "XTCLo.x3qfX"
    selector_click(driver,class_search)
    keyGo(driver,button_class_search,tag)



#LOGIN E GESTIONE POP-UP
def log(driver):
        #CARICA LA PAGINA WEB PASSANDO L'URL
        driver.get(URL)

        #FUNZIONE "selector_click" UTILIZZATA PER INTERAGIRE CON LA PAGINA WEB E I VARI POP-UP FACENDO USO DEI TAG HTML PRESENTI NELLA DOM
        #ALLA FUNZIONE VIENE PASSATO IL DRIVER DI SELENIUM E DI VOLTA IN VOLTA IL TAG HTML DA ANALIZZARE.
        selector_click(driver, class_cookie)

        #FUNZIONE "selector_keys" UTILIZZATA SEMPRE PER INTERAGIRE CON LA PAGINA WEB MA IN QUESTO CASO CIO CHE VA A FARE è LA COMPILAZIONE
        #DI VARI MODULI O, COME IN QUESTO CASO,  IL POPOLAMENTO DI CREDENZIALI
        selector_keys(driver, name_username, key_username)
        selector_keys(driver, name_password, key_pssw)

        selector_click(driver, class_log)
        selector_click(driver, class_NonOra)
        selector_click(driver, class_notifiche)



#MAIN DEL .py
def main():
   try:
       driver = webdriver.Chrome(DRIVEPATH)
       log(driver)
       #INTERFACCIA HOME E PREPARAZIONE ALLO SCRAPING
       ig_panel(driver)
       #SCRAPING DEI POSTs
       scrape(driver)
   finally:
           #time.sleep(8)
           time.sleep(5)
           driver.quit()


main()



