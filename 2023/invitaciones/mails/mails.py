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

#por_nombres(["Zenteno"])
#por_nombre("Goijman")
#papers_de("57193602956")
#datos["57195679171"]["mails"]

len(datos)
len(papers)


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

Le contactamos personalmente porque hemos visto que participa de un artículo donde se consideran aspectos de los métodos bayesianos. El equipo organizador de Bayes Plurinacional desea invitarle a la Escuela-Congreso Bayes Plurinacional 2024 a realizarse del 6 al 8 de agosto del 2024 en la Universidad Nacional de Salta (UNSa), con el apoyo de la Organización de Inteligencia Artificial de Latinoamérica (Khipu).

El año pasado la comunidad Bayes Plurinacional realizó con éxito el primer Congreso Bayesiano Plurinacional 2023. La diversidad disciplinar (desde física cuántica a antropología) y de regiones (8 países latinoamericanos) fue extraordinaria. Durante el congreso hubo un acuerdo respecto de la necesidad de contar con mayor cantidad de instancias de formación en métodos bayesianos en toda nuestra región. Por ello este año se decidió organizar la Escuela-Congreso Bayes Plurinacional 2024.

La **Escuela-Congreso Bayes Plurinacional 2024** será de carácter presencial y sin costo. Contará con talleres prácticos de todos los niveles (inicial, intermedio y avanzado), aplicaciones, exposiciones, mesas de debates y sesión de póster. La variedad de talleres, diseñados para inspirar, educar y conectar a los participantes, ofrecerá contenido relevante para el desarrollo profesional en todos los niveles de formación, desde estudiantes universitarios hasta personal calificado de empresas de primer nivel o investigadores formados. Le invitamos a proponer un taller, una charla, una mesa debate o un póster (o anunciar su participación) a través del formulario: https://bayesplurinacional.org/link/InscripcionSalta2024.html. Se reciben propuestas hasta el 30 de abril del 2024. Puede descargar la imagen para compartir en https://bayesplurinacional.org/link/VolanteSalta2024.html

De forma paralela e independiente se realizarán eventos virtuales permanentes, que incluye un Hackatón basado en inferencia, apuestas e intercambio de recursos. Las actividades son por naturaleza interdisciplinarias y están enfocadas en el aprendizaje práctico y conceptual de los métodos bayesianos (o aplicación estricta de las reglas de la probabilidad). Le invitamos a proponer un evento virtual utilizando el siguiente formulario https://bayesplurinacional.org/link/InscripcionEventosVirtuales.html


** ¿Dónde inscribirse? **
Su participación es posible en ambas modalidades.
- Regístre una propuesta para al evento presencial hasta el 30 de abril (o anuncie su participación antes del evento) en: https://bayesplurinacional.org/link/InscripcionSalta2024.html
- Regístre una propuesta para los eventos virtuales de forma permanente a través de: https://bayesplurinacional.org/link/InscripcionEventosVirtuales.html
- Si desea participar de la organización de Bayes Plurinacional, póngase en contacto respondiendo este correo.

** Auspiciantes Fundadores de Bayes Plurinacional **
Bayes Plurinacional ha abierto la convocatoria 2024 para establecer asociaciones con empresas e instituciones tecnológicas líderes en el mercado. El enfoque bayesiano (o aplicación estricta de las reglas de probabilidad) constituye la base de la inteligencia artificial (IA) y de todas las ciencias de datos debido a que garantiza la adopción de comportamientos óptimos en contextos de incertidumbre. Si bien hasta ahora no se ha propuesto nada mejor en términos prácticos, la aplicación del enfoque bayesiano se ha visto limitada históricamente debido al costo computacional asociado a la evaluación de todo el espacio de hipótesis. Sólo recientemente, en las vísperas del siglo 21, estos obstáculos han comenzado a ser superados en parte gracias a avances computacionales y algorítmicos modernos. Sin embargo, la inercia histórica hace que su desarrollo siga siendo incipiente, incluso en las Universidades más importantes de nuestro continente y por lo tanto en las empresas locales de más alto nivel de desarrollo tecnológico. En este contexto, nuestro objetivo es impulsar la Inteligencia Bayesiana en la América Plurinacional y los pueblos del Sur Global. Con el apoyo de la organización de Inteligencia Artificial de Latinoamérica Khipu, estamos profundizando todas las actividades necesarias para promover el inicio de la transición bayesiana en nuestro continente, creando las condiciones para la emergencia de la primera generación bayesiana. Los recursos humanos formados íntegramente en métodos bayesianos tienen capacidades que son todavía escasas a nivel mundial, que les permiten encontrar soluciones innovadoras a problemas complejos de cualquier clase. Asociarse como Auspiciante Fundador de Bayes Plurinacional le otorgará beneficios únicos a su empresa. Si desea explorar esta u otras opciones de patrocinio disponibles, póngase en contacto con Bayes Plurinacional a través de nuestro correo bayesplurinacional@gmail.com

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
##tree = html.fromstring(chrome.page_source)
##e = tree.xpath('//div[@id=":12q"]')[0]
##attach_xpath = e.getroottree().getpath(e)
#attach_xpath = '/html/body/div[27]/div/div/div/div[1]/div[2]/div[1]/div[1]/div/div/div/div[3]/div/div/div[4]/table/tbody/tr/td[2]/table/tbody/tr[2]/td/div/div/div[4]/table/tbody/tr/td[4]/div/div[1]/div/div/div'


contactos = pd.read_csv("contactos.csv")

no_enviar = set(contactos.iloc[:,0])
no_enviar.add("6507335048")
no_enviar.add("37119917600")
no_enviar.add("57205011847")
no_enviar.add("57200892844")
no_enviar.add("56287123600")
no_enviar.add("57204490428")

def personas():
    return sorted([(k,datos[k]) for k in datos if (len(datos[k]['mails'])>0) and (len(datos[k]['latinos'])>0) and not ("Brazil" in datos[k]['latinos']) ],key=lambda x: x[0])

castellano = personas()

#len(castellano)
#np.where(['Machain-Williams, Carlos' == persona[1]["nombre"] for persona in castellano ])

#set([q for k in datos for q in datos[k]])
i = 4323
while i < len(castellano):#len(castellano):
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
    input_cc.send_keys("metodosbayesianos@gmail.com")
    input_subject = chrome.find_elements(By.XPATH, "//input[@name='subjectbox']")[0]
    input_subject.clear()
    input_subject.send_keys('Bayes Plurinacional')
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
    i = i + 1
    print(i, ",", k, ",", cantidad_papers, ",", persona["nombre"])




sound.play()



chrome.close()








