from lxml import html
import nltk
import pycountry
import requests
import pickle
import csv
import pandas as pd
from collections import defaultdict
import re
import time
import os
from selenium.common.exceptions import MoveTargetOutOfBoundsException
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions

import numpy as np
from scipy.io.wavfile import write
import pygame

import time
from selenium.webdriver.common.by import By
import selenium
from unidecode import unidecode

from pygame import mixer
mixer.init()
sound=mixer.Sound("bell.wav")
sound2=mixer.Sound("bell2.wav")

def window_bounds(driver):
    win_upper_bound = driver.execute_script('return window.pageYOffset')
    win_left_bound = driver.execute_script('return window.pageXOffset')
    win_width = driver.execute_script('return document.documentElement.clientWidth')
    win_height = driver.execute_script('return document.documentElement.clientHeight')
    win_right_bound = win_left_bound + win_width
    win_lower_bound = win_upper_bound + win_height
    return win_left_bound, win_right_bound, win_upper_bound, win_lower_bound

def element_completely_viewable(driver, elem, win_left_bound, win_right_bound, win_upper_bound , win_lower_bound ):
    elem_left_bound = elem.location.get('x')
    elem_top_bound = elem.location.get('y')
    elem_width = elem.size.get('width')
    elem_height = elem.size.get('height')
    elem_right_bound = elem_left_bound + elem_width
    elem_lower_bound = elem_top_bound + elem_height
    #
    return all((win_left_bound <= elem_left_bound,
                win_right_bound >= elem_right_bound,
                win_upper_bound <= elem_top_bound,
                win_lower_bound >= elem_lower_bound)
              )


def autores(info_personas, xpath_personas, driver_paper):
    affil_links = []
    autor_links = []
    autor_posicion = []
    for i in range(len(info_personas)):#i=43
        # iks
        print(i)
        autor_posicion.append(i)
        print(1)
        ActionChains(driver_paper).move_to_element(info_personas[i]).click(info_personas[i]).perform()#info_personas[i].click()
        #
        print(2)
        affil_element = driver_paper.find_elements(By.XPATH, xpath_personas[i].split("/els-button")[0]+"/div/div/div/div/div/els-stack/els-stack[1]/els-stack//a" )
        list_affil = [e.get_attribute('href') for e in affil_element ]
        affil_links.append(list_affil)
        #
        print(3)
        autor_link_element = driver_paper.find_element(By.XPATH, xpath_personas[i].split("/els-button")[0]+"/div/div/div/div/div/els-stack/els-stack[1]/div//a" )
        autor_links.append("https://www.scopus.com/"+autor_link_element.get_attribute('href'))
        #
        print(4)
        x_elemento = driver_paper.find_element(by=By.XPATH, value= '//article/div[2]/section/div[2]/div[1]/div[2]//header/div[1]/els-button[1]')
        ActionChains(driver_paper).move_to_element(x_elemento).click(x_elemento).perform()
    print(5)
    return affil_links, autor_links, autor_posicion


# Set up the Firefox profile with the desired proxy settings
profile = webdriver.FirefoxProfile()
profile.set_preference("network.proxy.type", 1)
profile.set_preference("network.proxy.socks", "localhost")
profile.set_preference("network.proxy.socks_port", 2000)

#driver = webdriver.Firefox(firefox_profile=profile)
driver_paper = webdriver.Firefox(firefox_profile=profile)

url= "https://www.scopus.com/results/results.uri?sort=plf-f&src=s&st1=%28bayes+AND+NOT+%28%22naive+bayes%22%29%29+OR+%28%22causal+inference%22+AND+NOT+%28%22naive+bayes%22%29%29&st2=argentina+OR+chile+OR+uruguay+OR+paraguay+OR+bolivia+OR+per%c3%ba+OR+colombia+OR+venezuela+OR+brazil+OR+m%c3%a9xico+OR+cuba+OR+ecuador&sid=a83350921ff83885ce535de899e04f09&sot=b&sdt=b&sl=239&s=%28TITLE-ABS-KEY%28%28bayes+AND+NOT+%28%22naive+bayes%22%29%29+OR+%28%22causal+inference%22+AND+NOT+%28%22naive+bayes%22%29%29%29+AND+AFFILCOUNTRY%28argentina+OR+chile+OR+uruguay+OR+paraguay+OR+bolivia+OR+per%c3%ba+OR+colombia+OR+venezuela+OR+brazil+OR+m%c3%a9xico+OR+cuba+OR+ecuador%29%29&origin=searchbasic&editSaveSearch=&yearFrom=Before+1960&yearTo=2022"

url = "https://www.scopus.com/results/results.uri?sort=plf-f&src=s&st1=%28bayes+AND+NOT+%28%22naive+bayes%22%29%29+OR+%28%22causal+inference%22+AND+NOT+%28%22naive+bayes%22%29%29&st2=argentina+OR+chile+OR+uruguay+OR+paraguay+OR+bolivia+OR+per%c3%ba+OR+colombia+OR+venezuela+OR+brazil+OR+m%c3%a9xico+OR+cuba+OR+ecuador&sid=107c6cee5bce6d66a1a9e09145f25c0b&sot=b&sdt=b&sl=239&s=%28TITLE-ABS-KEY%28%28bayes+AND+NOT+%28%22naive+bayes%22%29%29+OR+%28%22causal+inference%22+AND+NOT+%28%22naive+bayes%22%29%29%29+AND+AFFILCOUNTRY%28argentina+OR+chile+OR+uruguay+OR+paraguay+OR+bolivia+OR+per%c3%ba+OR+colombia+OR+venezuela+OR+brazil+OR+m%c3%a9xico+OR+cuba+OR+ecuador%29%29&origin=searchbasic&editSaveSearch=&yearFrom=Before+1960&yearTo=2010"

#driver.get(url)
#tree = html.fromstring(driver.page_source)

#nombre_papers = tree.xpath('//a[@class="ddmDocTitle"]/text()')
#link_papers = tree.xpath('//a[@class="ddmDocTitle"]/@href')

#len(nombre_papers)
#len(link_papers )

#total = int(tree.xpath('//span[@class="resultsCount"]')[0].text.replace('\n','').replace(',',''))


driver_paper.get("https://www.scopus.com/record/display.uri?eid=2-s2.0-77950358311&origin=resultslist&sort=plf-f&src=s&st1=%28bayes+AND+NOT+%28%22naive+bayes%22%29%29+OR+%28%22causal+inference%22+AND+NOT+%28%22naive+bayes%22%29%29&st2=argentina+OR+chile+OR+uruguay+OR+paraguay+OR+bolivia+OR+per%c3%ba+OR+colombia+OR+venezuela+OR+brazil+OR+m%c3%a9xico+OR+cuba+OR+ecuador&nlo=&nlr=&nls=&sid=107c6cee5bce6d66a1a9e09145f25c0b&sot=b&sdt=b&sl=258&s=%28TITLE-ABS-KEY%28%28bayes+AND+NOT+%28%22naive+bayes%22%29%29+OR+%28%22causal+inference%22+AND+NOT+%28%22naive+bayes%22%29%29%29+AND+AFFILCOUNTRY%28argentina+OR+chile+OR+uruguay+OR+paraguay+OR+bolivia+OR+per%c3%ba+OR+colombia+OR+venezuela+OR+brazil+OR+m%c3%a9xico+OR+cuba+OR+ecuador%29%29+AND+PUBYEAR+%3c+2011&relpos=106&citeCnt=38&searchTerm=")



n_paper = 890
autores_datos = dict()
papers_datos = dict()

with open('autores_datos.pickle', 'rb') as handle:
    autores_datos = pickle.load(handle)

with open('papers_datos.pickle', 'rb') as handle:
    papers_datos = pickle.load(handle)

len(papers_datos)
len(autores_datos)

total = 2000

t=0; r=0
while t < 5:
    try:
        while n_paper < total:
            # Levanto la página del paper.
            tree_paper = html.fromstring(driver_paper.page_source)
            next_link_xpath = [e.getroottree().getpath(e) for e in tree_paper.xpath('//section/nav/ul/li[@class="nextLink"]') ][0]
            record_page_count_xpath = [e.getroottree().getpath(e) for e in tree_paper.xpath('//section/nav/ul/li[@class="recordPageCount"]') ][0]
            #
            current_number_of_paper = driver_paper.find_element(By.XPATH, record_page_count_xpath).text.split("of")
            n_paper = int(current_number_of_paper[0].replace(',',''))
            print("paper: ", n_paper )
            #
            personas_path = [e.getroottree().getpath(e) for e in tree_paper.xpath('//div[@data-testid="author-list"]')][0]
            info_personas = driver_paper.find_elements(By.XPATH, personas_path+'/div[1]/ul/li/els-button')
            xpath_personas = [e.getroottree().getpath(e) for e in tree_paper.xpath(personas_path+'/div[1]/ul/li/els-button') ]
            #
            nombre_personas = [e.text for e in info_personas ]
            #
            mails = [driver_paper.find_elements(By.XPATH, xpath_personas[i].split("/els-button")[0]+"/a" ) for i in range(len(info_personas))]
            mails = [ None if len(m)==0 else m[0].get_attribute("href") for m in mails]
            #
            #affil = driver_paper.find_elements(By.XPATH, "//section/div[2]/div[1]/ul/li/span" )
            #affil = [e.text for e in affil]
            #
            try:
                affil_links = []
                affil_texts = []
                autor_links = []
                autor_posicion = []
                for i in range(len(info_personas)):#i=0
                    # iks
                    print("Persona: ", i, ". ", end="")
                    autor_posicion.append(i)
                    print(1, end="")
                    try:
                        ActionChains(driver_paper).move_to_element(info_personas[i]).click(info_personas[i]).perform()#info_personas[i].click()
                    except MoveTargetOutOfBoundsException:
                        driver_paper.execute_script("arguments[0].scrollIntoView();", info_personas[i])
                        time.sleep(0.5)
                        info_personas = driver_paper.find_elements(By.XPATH, personas_path+'/div[1]/ul/li/els-button')
                        ActionChains(driver_paper).move_to_element(info_personas[i]).click(info_personas[i]).perform()
                    print(2, end="")
                    affil_element = driver_paper.find_elements(By.XPATH, xpath_personas[i].split("/els-button")[0]+"/div/div/div/div/div/els-stack/els-stack[1]/els-stack//a" )
                    list_affil = [e.get_attribute('href') for e in affil_element ]
                    affil_links.append(list_affil)
                    affil_texts.append([e.text for e in driver_paper.find_elements(By.XPATH, "//els-stack[1]/els-stack[1]/els-stack[1]/els-stack[1]/span" )])
                    #
                    print(3, end="")
                    autor_link_element = driver_paper.find_element(By.XPATH, xpath_personas[i].split("/els-button")[0]+"/div/div/div/div/div/els-stack/els-stack[1]/div//a" )
                    autor_links.append("https://www.scopus.com/"+autor_link_element.get_attribute('href'))
                    #
                    print(4,".")
                    #x_elemento = driver_paper.find_element(by=By.XPATH, value= '//header/div[1]/els-button[1]')
                    #ActionChains(driver_paper).move_to_element(x_elemento).click(x_elemento).perform()
                    ActionChains(driver_paper).move_to_element(info_personas[i]).click(info_personas[i]).perform()#info_personas[i].click()
                try:
                    journal_link = driver_paper.find_element(By.XPATH, "//article/div/div/div/a").get_attribute("href")
                except:
                    journal_link = ""
                try:
                    journal_name = driver_paper.find_element(By.XPATH, "//article/div/div/div/a").text
                except:
                    journal_name = ""
                try:
                    publication_date = int(driver_paper.find_element(By.XPATH, "//article/div/div/div").text.split(" ")[-1])
                except:
                    publication_date = 0
                paper_name = driver_paper.find_element(By.XPATH, "//section/div/div/h2").text
                doc_type = [e.text.split("\n")[1] for e in driver_paper.find_elements(By.XPATH, "//article/div[2]/aside/div[1]/div[1]/div[1]/dl") if "Document type\n" in e.text]
                source_type = [e.text.split("\n")[1] for e in driver_paper.find_elements(By.XPATH, "//article/div[2]/aside/div[1]/div[1]/div[1]/dl") if "Source type\n" in e.text]
                doi = [e.text.split("\n")[1] for e in driver_paper.find_elements(By.XPATH, "//article/div[2]/aside/div[1]/div[1]/div[1]/dl") if "DOI\n" in e.text]
                issn = [e.text.split("\n")[1] for e in driver_paper.find_elements(By.XPATH, "//article/div[2]/aside/div[1]/div[1]/div[1]/dl") if "ISSN\n" in e.text]
                try:
                    abstract_path = [e.getroottree().getpath(e) for e in tree_paper.xpath('//h3[@id="abstract"]')][0]
                    abstract = driver_paper.find_element(By.XPATH, abstract_path.split("h3")[0]+'div').text
                except:
                    abstract = "empty"
                try:
                    key_words = driver_paper.find_element(By.XPATH, "//article/div[3]/section[1]/div[1]/div[2]").text.split(";")
                except:
                    key_words = []
                autor_id = [a.split("authorId=")[1].split("&")[0] for a in autor_links]
                key_paper = (autor_id[0], paper_name)
                if not (key_paper in papers_datos):
                    papers_datos[key_paper] = {"titulo": paper_name, "abstract": abstract, "palabras": key_words, "ISSN": issn, "DOI": doi, "autores": autor_id, "journal": journal_name, "source_type": source_type, "document_type": doc_type, "publication_date": publication_date  }
                #
                n_personas = len(nombre_personas)
                #
                #nombre_personas
                mails = [m.split('mailto:')[1] if not (m is None) and ('mailto:' in m) else m for m in mails ]
                #affil_links
                #affil_texts#sum(affil_texts, [])
                #autor_links
                #
                paises = []
                latino = []
                for i in range(n_personas):
                    paises.append([])
                    for a in affil_texts[i]:
                        try:
                            paises[-1].append(pycountry.countries.search_fuzzy(a.split(",")[-1])[0].name)
                        except:
                            paises[-1].append("desconocido")
                    latino.append([c for c in paises[-1] if c in ['Argentina', 'Uruguay', 'Chile', 'Paraguay', 'Bolivia, Plurinational State of', 'Peru', 'Colombia', 'Ecuador', 'Venezuela, Bolivarian Republic of', 'Cuba',  'Mexico', 'Brazil', 'Nicaragua', 'Honduras', 'Guatemala'] ])
                for a in range(n_personas):
                    if not (autor_id[a] in autores_datos):
                        autores_datos[autor_id[a]] = {"nombre": nombre_personas[a], "paises": set(paises[a]), "latinos": set(latino[a]), "mails": set() if mails[a] is None else set([mails[a]]), "affil": set(affil_texts[a]), "papers": set([(autor_posicion[a], paper_name)]) }
                    else:
                        autores_datos[autor_id[a]]["paises"].update(set(paises[a]))
                        autores_datos[autor_id[a]]["latinos"].update(set(latino[a]))
                        autores_datos[autor_id[a]]["affil"].update(set(affil_texts[a]))
                        autores_datos[autor_id[a]]["papers"].update(set([(autor_posicion[a], paper_name)]))
                        if not (mails[a] is None):
                            autores_datos[autor_id[a]]["mails"].update(set([mails[a]]))
                if n_paper%10 == 0:
                    with open('autores_datos.pickle', 'wb') as handle:
                        pickle.dump(autores_datos, handle, protocol=pickle.HIGHEST_PROTOCOL)
                    with open('papers_datos.pickle', 'wb') as handle:
                        pickle.dump(papers_datos, handle, protocol=pickle.HIGHEST_PROTOCOL)
                next_paper = driver_paper.find_element(By.XPATH, next_link_xpath)
                try:
                    ActionChains(driver_paper).move_to_element(next_paper).click(next_paper).perform()
                except MoveTargetOutOfBoundsException:
                    driver_paper.execute_script("arguments[0].scrollIntoView();", next_paper)
                    time.sleep(0.5)
                    next_paper = driver_paper.find_element(By.XPATH, next_link_xpath)
                    ActionChains(driver_paper).move_to_element(next_paper).click(next_paper).perform()
                print(driver_paper.current_url)
                time.sleep(6)
                t=0
                r=0
            except:
                print("except")
                time.sleep(2)
                r+=1
                if r > 5:
                    sound.play()
    except:
        t+=1
        time.sleep(1)

sound.play()
sound.play()
sound.play()




driver_paper.close()

