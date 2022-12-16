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

driver_paper.get(link_papers[0] )
tree_paper = html.fromstring(driver_paper.page_source)

autores_nombres = tree_paper.xpath('//els-button/text()')


# Necesitamos identiificar a los links de los autores, y sus pertenencias.

###############################################################

# Abro la pestaña escondida del primer autor
info_personas = driver_paper.find_elements(by=By.TAG_NAME, value= 'els-button')
ActionChains(driver_paper).move_to_element(info_personas[0]).click(info_personas[0]).perform()
info_personas[0].click()

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
