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
import undetected_chromedriver as uc

from datetime import date

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


with open('../perfiles/scopus/autores_datos.pickle', 'rb') as handle:
    datos = pickle.load(handle)

with open('../perfiles/scopus/papers_datos.pickle', 'rb') as handle:
    papers = pickle.load(handle)



def papers_de(k, full=False):
    return [(p, papers[p]["publication_date"], papers[p]["cited_by"], papers[p]["abstract"]) if full else (p, papers[p]["publication_date"], papers[p]["cited_by"])  for p in papers if k in papers[p]["autores"]]

def por_nombre(nom):
    return [(datos[k]["nombre"],k, len(papers_de(k)) ) for k in datos if nom in datos[k]["nombre"]]


#por_nombre("Goijman")
#papers_de("24464407100", True)
#datos["37119917600"]["mails"]

len(datos)
len(papers)


# Set up the Firefox profile with the desired proxy settings
profile = webdriver.FirefoxProfile()
profile.set_preference("network.proxy.type", 1)
profile.set_preference("network.proxy.socks", "localhost")
profile.set_preference("network.proxy.socks_port", 2000)
firefox = webdriver.Firefox(firefox_profile=profile)


chrome = uc.Chrome()
chrome.get("https://www.google.com/gmail/about/")

######################################
######################################
######################################


mensaje = """Buen día {} {},

Le escribimos personalmente porque vimos que tiene algunos trabajos con el enfoque bayesiano de la probabilidad. Nos ponemos en contacto para invitarle a participar del primer Congreso Bayesiano Plurinacional, que tendrá lugar los días 4 y 5 de agosto en Santiago del Estero, Argentina. El objetivo es fortalecer las comunidades bayesianas en América Latina y promover el potencial de los métodos bayesianos en la academia, la industria, el Estado y la sociedad.

El Congreso es una oportunidad para debatir una amplia gama de temas, con algo interesante para todos los gustos. El evento contará con charlas de 10 a 15 minutos, con sesiones de pósters, y con talleres sobre programación probabilística ofrecidos por miembros de PyMC/ArviZ. Hasta el 31 de marzo están abiertas las inscripciones, enviando un resumen breve de no más de 300 palabras a [1].

Debido a que un encuentro presencial de dos días no nos va a alcanzar, hemos decido organizar un seminario virtual a lo largo del año. Las inscripciones permanecerán abiertas de forma permanente hasta el 1 de agosto. Se puede anunciar la intención de participar enviando un breve resumen [2], que puede ser el mismo que el de la charla presencial. Las grabaciones quedarán disponibles en el canal de Youtube.

Además, en los próximos días lanzaremos un Hackatón por nuestras redes sociales. (Para más detalles vea la página bayesdelsur.com.ar)

Esperamos vivamente su respuesta. Si quiere participar de la organización, no dude en contactarnos.

En nombre del equipo de organización, le saluda muy atentamente Gustavo Landfried (correo en copia).

[1] https://bit.ly/FormularioCongresoBayesiano2023
[2] https://bit.ly/SeminarioComunidadBayesiana

Redes sociales
- Página web oficial: https://bayesdelsur.com.ar
- Linkedin: https://www.linkedin.com/company/bayes-plurinacional/
- Twitter: https://twitter.com/BayesDelSur
- Mastodon: https://bayes.club/@BayesDelSur
- Youtube: https://www.youtube.com/@bayesdelsur
"""


remensaje = """Buen día {} {},

Nos ponemos en contacto nuevamente desde la organización del Congreso Bayesiano Plurinacional para recordarle que el 31 de marzo es la fecha límite para inscribirse a las charlas y las sesiones de póster enviando un resumen breve de no más de 300 palabras a [1]. El evento contará además con talleres sobre programación probabilística ofrecidos por miembros de PyMC/ArviZ.

Debido a que un encuentro presencial de dos días no nos va a alcanzar, hemos decido organizar un seminario virtual a lo largo del año. Las inscripciones permanecerán abiertas de forma permanente hasta el 1 de agosto. Se puede anunciar la intención de participar enviando un breve resumen a [2], que puede ser el mismo que el de la charla presencial. Las grabaciones quedarán disponibles en el canal de Youtube.

Además, en los próximos días lanzaremos un Hackatón por nuestras redes sociales. (Para más detalles vea la página bayesdelsur.com.ar)

Esperamos vivamente su respuesta.

En nombre del equipo de organización, le saluda muy atentamente Gustavo Landfried (correo en copia).

[1] https://bit.ly/FormularioCongresoBayesiano2023
[2] https://bit.ly/SeminarioComunidadBayesiana

Redes sociales
- Página web oficial: https://bayesdelsur.com.ar
- Linkedin: https://www.linkedin.com/company/bayes-plurinacional/
- Twitter: https://twitter.com/BayesDelSur
- Mastodon: https://bayes.club/@BayesDelSur
- Youtube: https://www.youtube.com/@bayesdelsur
"""



redactar = chrome.find_elements(By.CLASS_NAME, "z0")[0]
redactar = redactar.find_elements(By.XPATH, ".//div")[0]

#tree = html.fromstring(chrome.page_source)
#e = tree.xpath('//input[@id=":1cy"]')[0]
#input_mail_xpath = e.getroottree().getpath(e)
input_mail_xpath == '/html/body/div[25]/div/div/div/div[1]/div[2]/div[1]/div[1]/div/div/div/div[3]/div/div/div[4]/table/tbody/tr/td[2]/form/div[1]/table/tbody/tr[1]/td[2]/div/div/div[1]/div/div[3]/div/div/div/div/div/input'
#tree = html.fromstring(chrome.page_source)
#e = tree.xpath('//div[@id=":r3"]')[0]
#input_texto_xpath = e.getroottree().getpath(e)
input_texto_xpath = '/html/body/div[25]/div/div/div/div[1]/div[2]/div[1]/div[1]/div/div/div/div[3]/div/div/div[4]/table/tbody/tr/td[2]/table/tbody/tr[1]/td/div/div[1]/div[2]/div[3]/div/table/tbody/tr/td[2]/div[2]/div'
#tree = html.fromstring(chrome.page_source)
#e = tree.xpath('//img[@id=":lk"]')[0]
#close_input_xpath = e.getroottree().getpath(e)
close_input_xpath = '/html/body/div[25]/div/div/div/div[1]/div[2]/div[1]/div[1]/div/div/div/div[2]/div/div[2]/div/div/div/div/table/tbody/tr/td[2]/img[3]'
#tree = html.fromstring(chrome.page_source)
#e = tree.xpath('//div[@id=":oa"]')[0]
#enviar_xpath = e.getroottree().getpath(e)
enviar_xpath = '/html/body/div[25]/div/div/div/div[1]/div[2]/div[1]/div[1]/div/div/div/div[3]/div/div/div[4]/table/tbody/tr/td[2]/table/tbody/tr[2]/td/div/div/div[4]/table/tbody/tr/td[1]/div/div[2]/div[1]'
#tree = html.fromstring(chrome.page_source)
#e = tree.xpath('//span[@id=":sr"]')[0]
#boton_cc = e.getroottree().getpath(e)
boton_cc_xpath = '/html/body/div[25]/div/div/div/div[1]/div[2]/div[1]/div[1]/div/div/div/div[3]/div/div/div[4]/table/tbody/tr/td[2]/form/div[1]/table/tbody/tr[1]/td[2]/div/div/div[2]/span/span/span[1]'
#tree = html.fromstring(chrome.page_source)
#e = tree.xpath('//input[@id=":36n"]')[0]
#cc_xpath = e.getroottree().getpath(e)
cc_xpath = '/html/body/div[25]/div/div/div/div[1]/div[2]/div[1]/div[1]/div/div/div/div[3]/div/div/div[4]/table/tbody/tr/td[2]/form/div[1]/table/tbody/tr[2]/td[2]/div/div/div[1]/div/div[3]/div/div/div/div/div/input'

contactos = pd.read_csv("contactos.csv")

no_enviar = set(contactos.iloc[:,0])
no_enviar.add("6507335048")
no_enviar.add("37119917600")

def personas():
    return sorted([(k,datos[k]) for k in datos if (len(datos[k]['mails'])>0) and (len(datos[k]['latinos'])>0) and not ("Brazil" in datos[k]['latinos']) ],key=lambda x: x[0])

castellano = personas()

#set([q for k in datos for q in datos[k]])
i = 1234
while i < len(castellano):
    k, persona = castellano[i]
    url="https://www.scopus.com/authid/detail.uri?authorId={}".format(k)
    firefox.get(url)
    ActionChains(chrome).move_to_element(redactar).click(redactar).perform()
    time.sleep(1)
    try:
        apellido, nombre = firefox.find_element(By.XPATH,"//h1[@data-testid='author-profile-name']").text.split(", ")
    except:
        nombre = persona["nombre"]
        apellido = ""
    cantidad_papers = len(persona["papers"])
    print(i, ",", k, ",", apellido, ",", nombre, ",", cantidad_papers, ",", persona["nombre"])
    mails = persona["mails"]
    input_mail = chrome.find_element(By.XPATH, input_mail_xpath )
    #input_mail.get_attribute("id")
    ActionChains(chrome).move_to_element(input_mail).click(input_mail).perform()
    input_mail.clear()
    input_mail.send_keys(",".join(mails))
    boton_cc = chrome.find_element(By.XPATH, boton_cc_xpath )
    ActionChains(chrome).move_to_element(boton_cc).click(boton_cc).perform()
    input_cc = chrome.find_element(By.XPATH, cc_xpath)
    input_cc.send_keys("gustavolandfried@gmail.com")
    input_subject = chrome.find_elements(By.XPATH, "//input[@name='subjectbox']")[0]
    input_subject.clear()
    input_subject.send_keys('Comunidad bayesiana')
    input_texto = chrome.find_element(By.XPATH, input_texto_xpath)
    input_texto.clear()
    input_texto.send_keys(mensaje.format(nombre, apellido))
    enviar = chrome.find_element(By.XPATH, enviar_xpath)
    if not (k in no_enviar):
        ActionChains(chrome).move_to_element(enviar).click(enviar).perform()
        time.sleep(1.5)
    else:
        close_mail = chrome.find_element(By.XPATH, close_input_xpath )
        ActionChains(chrome).move_to_element(close_mail).click(close_mail).perform()
    i = i + 1



sound.play()








chrome.close()








