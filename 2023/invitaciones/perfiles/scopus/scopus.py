from lxml import html
import requests
import csv
import pandas as pd
from collections import defaultdict
import re
import time
import os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
from selenium.webdriver.common.action_chains import ActionChains

import time
from selenium.webdriver.common.by import By
import selenium
from unidecode import unidecode


# Set up the Firefox profile with the desired proxy settings
profile = webdriver.FirefoxProfile()
profile.set_preference("network.proxy.type", 1)
profile.set_preference("network.proxy.socks", "localhost")
profile.set_preference("network.proxy.socks_port", 2000)

driver = webdriver.Firefox(firefox_profile=profile)
driver_paper = webdriver.Firefox(firefox_profile=profile)
driver_persona = webdriver.Firefox(firefox_profile=profile)

url= "https://www.scopus.com/results/results.uri?sort=plf-f&src=s&st1=bayes&st2=argentina+OR+chile+OR+uruguay+OR+paraguay+OR+bolivia+OR+per%c3%ba+OR+colombia+OR+venezuela+OR+brasil+OR+m%c3%a9xico+OR+Cuba+OR+ecuador&sid=bf9c53c34cc20d2a645a1d3d875e9e17&sot=b&sdt=b&sl=165&s=%28TITLE-ABS-KEY%28bayes%29+AND+AFFILCOUNTRY%28argentina+OR+chile+OR+uruguay+OR+paraguay+OR+bolivia+OR+per%c3%ba+OR+colombia+OR+venezuela+OR+brasil+OR+m%c3%a9xico+OR+Cuba+OR+ecuador%29%29&offset=1&origin=recordpage"

driver.get(url)

tree = html.fromstring(driver.page_source)

nombre_papers = tree.xpath('//a[@class="ddmDocTitle"]/text()')
link_papers = tree.xpath('//a[@class="ddmDocTitle"]/@href')

len(nombre_papers)
len(link_papers )

# Levanto la página del paper.
driver_paper.get(link_papers[3] )
tree_paper = html.fromstring(driver_paper.page_source)


## Busco las personas, abro la ventana y busco link

links_elements_en_paper = driver_paper.find_elements(by=By.TAG_NAME, value= 'a')

info_personas = driver_paper.find_elements(by=By.TAG_NAME, value= 'els-button')
nombre_personas = [e.text for e in info_personas ]
xpath_personas = [e.getroottree().getpath(e) for e in tree_paper.xpath('//els-button') ]

mails = [driver_paper.find_elements(By.XPATH, xpath_personas[i].split("/els-button")[0]+"/a" ) for i in range(len(info_personas))]
mails = [ None if len(m)==0 else m[0].get_attribute("href") for m in mails]

affil = [driver_paper.find_elements(By.XPATH, xpath_personas[i].split("/els-button")[0]+"/span" )[0].text for i in range(len(info_personas))]

affil_links = []
autor_links = []

#driver.execute_script("arguments[0].scrollIntoView(true);", info_personas[i]);

for i in range(len(info_personas)):#i=0
    # iks
    print(1)
    ActionChains(driver_paper).move_to_element(info_personas[i]).click(info_personas[i]).perform()#info_personas[i].click()
    #
    print(2)
    affil_element = driver_paper.find_elements(By.XPATH, xpath_personas[i].split("/els-button")[0]+"/div/div/div/div/div/els-stack/els-stack[1]/els-stack//a" )
    list_affil = [e.get_attribute('href') for e in affil_element ]
    affil_links.append(list_affil)
    #
    print(3)
    autor_link_element = driver_paper.find_element(By.XPATH, xpath_personas[i].split("/els-button")[0]+"/div/div/div/div/div/els-stack/els-stack[1]/div/els-stack/els-button" )
    autor_links.append("https://www.scopus.com/"+autor_link_element.get_attribute('href'))
    #
    print(4)
    ActionChains(driver_paper).move_to_element(info_personas[i]).click(info_personas[i]).perform()
    print(5)



# Hasta aca funciona
##############################################################


links_elements_en_paper2 = driver_paper.find_elements(by=By.TAG_NAME, value= 'a')
new_link = list(set(links_elements_en_paper2 ) - set(links_elements_en_paper))[0]
new_link.get_attribute('href')

info_personas2 = driver_paper.find_elements(by=By.TAG_NAME, value= 'els-button')
len(info_personas2 )
href2 = [info_personas2[i].get_attribute('href') for i in range(len(info_personas2))]
[h for h in href2 if (not (h==None)) and ("authid/detail." in h)]
[e.text for e in info_personas2 ]

links_elements_autores = [e for e in links_elements_en_paper  if not (e.get_attribute('href') == None) and "authorId" in e.get_attribute('href') ]
links_autores = [e.get_attribute('href') for e in links_elements_en_paper  if not (e.get_attribute('href') == None) and "authorId" in e.get_attribute('href')
[ l.split("authorId=")[1] for l in links_autores ]


links_elements_en_paper = driver_paper.find_elements(by=By.TAG_NAME, value= 'a')


autores_nombres = tree_paper.xpath('//els-button/text()')

autores_elements = autores_nombres = tree_paper.xpath('//els-button/text()')
('//els-button/text()')




mail = tree_paper.xpath('//div[@data-testid="author-list"]//a/@href')

autor_links = [ l for l in tree_paper.xpath('//a/@href')]
autor_link_elements =  [ x for x, l in zip(tree_paper.xpath('//a'), tree_paper.xpath('//a/@href')) if "authorId" in l ]

for e in autor_link_elements:
    print(e.get_attribute('xpath'))





# Necesitamos identiificar a los links de los autores, y sus pertenencias.

###############################################################

# Abro la pestaña escondida del primer autor

##len(info_personas[0].find_elements(By.XPATH, "//a[@href]"))
##driver_paper.find_elements(By.XPATH, ".//a[@href]")
##get_attribute('href')


tree_temporal = html.fromstring(driver_paper.page_source)
autores = tree_temporal.xpath('//div[@data-testid="author-list"]')[0]
mail = tree_temporal.xpath('//div[@data-testid="author-list"]//a/@href')
#tree_temporal.xpath('//section[@data-testid="document-details-header"]//a/@href')

autor_links = [ l for l in tree_temporal.xpath('//a/@href') if "authorId" in l]
len(autor_links )
href="/authid/detail.uri?authorId=57983598100&origin=recordPage"
