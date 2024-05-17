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

def por_nombres(noms):
    res = []
    for k in datos:
        checks = [n in datos[k]["nombre"] for n in noms]
        if sum(checks) == len(noms):
            res.append((datos[k]["nombre"],k, len(papers_de(k))))
    return res

len(datos)
len(papers)
# por_nombres(["Juliana Sterli"])
# papers_de('6507675654', full=False)

##Set up the Firefox profile with the desired proxy settings
#profile = webdriver.FirefoxProfile()
#profile.set_preference("network.proxy.type", 1)
#profile.set_preference("network.proxy.socks", "localhost")
#profile.set_preference("network.proxy.socks_port", 2000)
#firefox = webdriver.Firefox(firefox_profile=profile)


chrome = uc.Chrome()
chrome.get("https://www.google.com/gmail/about/")


######################################
######################################
######################################


mensaje = """Buen día {} {},

Le contactamos personalmente porque hemos visto que participa de un artículo donde se consideran aspectos de los métodos bayesianos. El enfoque bayesiano (o aplicación estricta de las reglas de probabilidad) constituye la base de todas las ciencias empíricas (o ciencias con datos), incluyendo la Inteligencia Artificial. Si bien hasta ahora no se ha propuesto nada mejor en términos prácticos, su aplicación se ha visto limitada históricamente debido al costo computacional asociado a la evaluación de todo el espacio de hipótesis.

Para promover la Inteligencia Bayesiana en la América Plurinacional, el equipo organizador de Bayes Plurinacional desea invitarle a la Escuela-Congreso (presencial y sin costo) a realizarse del 6 al 8 de agosto del 2024 en la Universidad Nacional de Salta (Argentina), con el apoyo de la Organización de Inteligencia Artificial de América Latina (Khipu). Le invitamos a que proponga un taller, una charla, una mesa debate o un póster (o anuncie su participación) antes del 3 de mayo ingresando a https://bayesplurinacional.org/link/InscripcionSalta2024.html o a nuestra página web bayesplurinacional.org. Solo se requiere subir un breve resumen de la propuesta.

Si no puede participar presencialmente, también organizaremos eventos virtuales que se realizarán de forma paralela e independiente. Le invitamos a proponer un taller, charla, u otro tipo de evento virtual a través del siguiente formulario https://bayesplurinacional.org/link/InscripcionEventosVirtuales.html

** Auspiciantes Fundadores de Bayes Plurinacional **
Bayes Plurinacional ha abierto la convocatoria 2024 para establecer asociaciones con empresas e instituciones tecnológicas líderes en el mercado. Con el apoyo de la organización de Inteligencia Artificial de Latinoamérica Khipu, estamos promoviendo la formación y aplicación de los métodos bayesianos en nuestro continente. Los recursos humanos formados íntegramente en métodos bayesianos tienen capacidades que son todavía escasas a nivel mundial. Si desea asociarse como Auspiciante Fundador de Bayes Plurinacional o conocer otras opciones de patrocinio disponibles, contáctenos a través de nuestro correo bayesplurinacional@gmail.com

** Promoviendo la Inteligencia Bayesiana en la América Plurinacional y los pueblos del Sur Global **

Le saluda muy atentamente el equipo organizador de Bayes Plurinacional.

Nuestras redes:
- Web: https://bayesplurinacional.org
- Grupo de mails: https://groups.google.com/u/1/g/bayes-plurinacional
- Linkedin: https://www.linkedin.com/company/bayes-plurinacional/
- Twitter (X): https://twitter.com/BayesPlural
- Instagram: https://www.instagram.com/bayesplurinacional
"""


redactar = chrome.find_elements(By.CLASS_NAME, "z0")[0]
redactar = redactar.find_elements(By.XPATH, ".//div")[0]

tree = html.fromstring(chrome.page_source)
e = tree.xpath('//input[@aria-label="Destinatarios en Para"]')[0]
input_mail_xpath = e.getroottree().getpath(e)
e = tree.xpath('//div[@aria-label="Cuerpo del mensaje"]')[0]
input_texto_xpath = e.getroottree().getpath(e)
e = tree.xpath('//div[@aria-label="Enviar ‪(Ctrl-Enter)‬"]')[0]
enviar_xpath = e.getroottree().getpath(e)
e = tree.xpath('//span[@aria-label="Agregar destinatarios a Cc ‪(Ctrl-Mayús-C)‬"]')[0]
boton_cc_xpath = e.getroottree().getpath(e)
tree = html.fromstring(chrome.page_source)
e = tree.xpath('//input[@aria-label="Destinatarios en Cc"]')[0]
cc_xpath = e.getroottree().getpath(e)
e = tree.xpath('//img[@aria-label="Guardar y cerrar"]')[0]
close_input_xpath = e.getroottree().getpath(e)


contactos = pd.read_csv("contactos.csv")

no_enviar = set(contactos.iloc[:,0])
no_enviar.add("6507335048")
no_enviar.add("37119917600")
no_enviar.add("57205011847")
no_enviar.add("57200892844")
no_enviar.add("56287123600")
no_enviar.add("57204490428")
no_enviar.add("7401545071")
no_enviar.add("57195288338")
no_enviar.add("36933923200")
no_enviar.add("7006111690")
no_enviar.add("23049951900")
no_enviar.add("23390888100")
no_enviar.add("22233766300")
no_enviar.add("15762187000")
no_enviar.add("55315383600")
no_enviar.add("57730251900")
no_enviar.add("57729955000")
no_enviar.add("55995941700")
no_enviar.add("56013571600")#PRoblemas con el correo
no_enviar.add("56236697700")#PRoblemas con el correo
no_enviar.add("56728594200")#Problemas con el correo
no_enviar.add("56989944200")#Problemas con el correo
no_enviar.add("57014110400")#Problemas con el correo
no_enviar.add("57188557062")#Problemas con el correo
no_enviar.add("57768813900")
no_enviar.add("49561184500")#repetido
no_enviar.add("23097366400")
no_enviar.add("23092376000")
no_enviar.add("6603356992")#Jubilado

# por_nombres(["Cantet"])
# papers_de('6507675654', full=False)


def personas():
    return sorted([(k,datos[k]) for k in datos if (len(datos[k]['mails'])>0) and (len(datos[k]['latinos'])>0) and not ("Brazil" in datos[k]['latinos']) ],key=lambda x: x[0])

castellano = personas()

#len(castellano)
#np.where(['Cristina, Juan' == persona[1]["nombre"] for persona in castellano ])

#set([q for k in datos for q in datos[k]])
i = 3783
while i < 3900:#3900len(castellano):
    k, persona = castellano[i]
    #url="https://www.scopus.com/authid/detail.uri?authorId={}".format(k)
    #firefox.get(url)
    ActionChains(chrome).move_to_element(redactar).click(redactar).perform()
    time.sleep(0.1)
    #try:i
    #apellido, nombre = firefox.find_element(By.XPATH,"//h1[@data-testid='author-profile-name']").text.split(", ")
    #except:
    #nombre = persona["nombre"]
    #apellido = ""
    apellidoNombre = persona["nombre"].split(", ")
    apellido, nombre = apellidoNombre if len(apellidoNombre)==2 else (persona["nombre"], "")
    cantidad_papers = len(persona["papers"])
    #print(i, ",", k, ",", apellido, ",", nombre, ",", cantidad_papers, ",", persona["nombre"])
    mails = list(persona["mails"])
    #mails.append("metodosbayesianos@gmail.com")
    input_mail = chrome.find_element(By.XPATH, input_mail_xpath )
    #input_mail.get_attribute("id")
    ActionChains(chrome).move_to_element(input_mail).click(input_mail).perform()
    input_mail.clear()
    input_mail.send_keys(",".join(mails))
    boton_cc = chrome.find_element(By.XPATH, boton_cc_xpath )
    ActionChains(chrome).move_to_element(boton_cc).click(boton_cc).perform()
    input_cc = chrome.find_element(By.XPATH, cc_xpath)
    input_cc.send_keys("gustavolandfried@gmail.com, metodosbayesianos@gmail.com")
    input_subject = chrome.find_elements(By.XPATH, "//input[@name='subjectbox']")[0]
    input_subject.clear()
    input_subject.send_keys('Escuela-Congreso Bayes Plurinacional 2024. Últimos días para presentar propuestas.')
    input_texto = chrome.find_element(By.XPATH, input_texto_xpath)
    input_texto.clear()
    input_texto.send_keys(mensaje.format(nombre, apellido))
    enviar = chrome.find_element(By.XPATH, enviar_xpath)
    if not (k in no_enviar):
        ActionChains(chrome).move_to_element(enviar).click(enviar).perform()
        time.sleep(0.2)
    else:
        close_mail = chrome.find_element(By.XPATH, close_input_xpath )
        ActionChains(chrome).move_to_element(close_mail).click(close_mail).perform()
    print(i, ",", k, ",", cantidad_papers, ",", persona["nombre"])
    i = i + 1



sound.play()



chrome.close()








