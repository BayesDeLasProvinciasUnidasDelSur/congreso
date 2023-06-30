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

#por_nombres(["Rios", "Gonzalo"])
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


mensaje = """Buen día {} {}

Tenemos el agrado de escribirle en el contexto de creación y plena actividad de la Comunidad Bayesiana Plurinacional.

Con el objetivo de impulsar el enfoque bayesiano en nuestra región, un grupo de especialistas latinoamericanos nos encontraremos del 4 al 6 de agosto en el Congreso Bayesiano que se realizará en Santiago del Estero, Argentina. Además, hemos comenzado a organizar un Seminario virtual permanente y un Hackatón virtual. Las actividades son por naturaleza interdisciplinarias y están enfocadas en la epistemología y metodología común a todas las ciencias con datos: el enfoque bayesiano (o aplicación estricta de las reglas de la probabilidad).

Hace más de un año, junto con especialistas de diversas actividades productivas que trabajan con el enfoque bayesiano, decidimos desarrollar lo que hoy llamamos Bayes Plurinacional. Analizando los artículos científicos con afiliación en latinoamérica encontramos que la comunidad bayesiana es más grande de lo que parece. Sin embargo, a través del contacto directo pudimos verificar que la comunidad está muy desconectada, sus protagonistas no se conocen todavía. En cualquier caso, la transición bayesiana es un proceso global que se está acelerando.

En este contexto, queremos invitarle a que participe de forma activa y creativa de la orientación y las acciones de Bayes Plurinacional. El objetivo es crear una organización al servicio de la comunidad bayesiana latinoamericana, caribeña y del sur global. El principal objetivo para el año 2023-2024 es dotar de estructura a la comunidad, asignando roles y formas de cambio, para que la comunidad Bayes Plurinacional tome vida propia y se desarrolle de manera autónoma y descentralizada.

Esperamos que este contacto virtual se transforme en un vínculo personal a largo plazo con algunas de las comunidades bayesianas que ya existen a lo largo y ancho de nuestro continente.

En nombre de la comunidad Bayes Plurinacional, le saluda muy atentamente los equipos organizadores del Congreso: Bayes del Sur [1] y Laboratorios de Métodos Bayesianos (en copia).

[1] https://bayesdelsur.com.ar

Redes sociales
- Linkedin: https://www.linkedin.com/company/bayes-plurinacional/
- Twitter: https://twitter.com/BayesDelSur
- Youtube: https://www.youtube.com/@bayesdelsur
"""


redactar = chrome.find_elements(By.CLASS_NAME, "z0")[0]
redactar = redactar.find_elements(By.XPATH, ".//div")[0]

#tree = html.fromstring(chrome.page_source)
#e = tree.xpath('//input[@id=":uf"]')[0]
#input_mail_xpath = e.getroottree().getpath(e)
input_mail_xpath = '/html/body/div[24]/div/div/div/div[1]/div[2]/div[1]/div[1]/div/div/div/div[3]/div/div/div[4]/table/tbody/tr/td[2]/form/div[1]/table/tbody/tr[1]/td[2]/div/div/div[1]/div/div[3]/div/div/div/div/div/input'
#tree = html.fromstring(chrome.page_source)
#e = tree.xpath('//div[@id=":rr"]')[0]
#input_texto_xpath = e.getroottree().getpath(e)
input_texto_xpath = 'html/body/div[24]/div/div/div/div[1]/div[2]/div[1]/div[1]/div/div/div/div[3]/div/div/div[4]/table/tbody/tr/td[2]/table/tbody/tr[1]/td/div/div[1]/div[2]/div[3]/div/table/tbody/tr/td[2]/div[2]/div'
#tree = html.fromstring(chrome.page_source)
#e = tree.xpath('//img[@id=":mv"]')[0]
#close_input_xpath = e.getroottree().getpath(e)
close_input_xpath = '/html/body/div[28]/div/div/div/div[1]/div[2]/div[1]/div[1]/div/div/div/div[2]/div/div[2]/div/div/div/div/table/tbody/tr/td[2]/img[3]'
#tree = html.fromstring(chrome.page_source)
#e = tree.xpath('//div[@id=":q8"]')[0]
#enviar_xpath = e.getroottree().getpath(e)
enviar_xpath = '/html/body/div[28]/div/div/div/div[1]/div[2]/div[1]/div[1]/div/div/div/div[3]/div/div/div[4]/table/tbody/tr/td[2]/table/tbody/tr[2]/td/div/div/div[4]/table/tbody/tr/td[1]/div/div[2]/div[1]'
#tree = html.fromstring(chrome.page_source)
#e = tree.xpath('//span[@id=":s3"]')[0]
#boton_cc_xpath = e.getroottree().getpath(e)
boton_cc_xpath = '/html/body/div[28]/div/div/div/div[1]/div[2]/div[1]/div[1]/div/div/div/div[3]/div/div/div[4]/table/tbody/tr/td[2]/form/div[1]/table/tbody/tr[1]/td[2]/div/div/div[2]/span/span/span[1]'
#tree = html.fromstring(chrome.page_source)
#e = tree.xpath('//input[@id=":18v"]')[0]
#cc_xpath = e.getroottree().getpath(e)
cc_xpath = '/html/body/div[28]/div/div/div/div[1]/div[3]/div[1]/div[1]/div/div/div/div[3]/div/div/div[4]/table/tbody/tr/td[2]/form/div[1]/table/tbody/tr[3]/td[2]/div/div/div[1]/div/div[3]/div/div/div/div/div/input'

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

#set([q for k in datos for q in datos[k]])
i = 3387
while i < 3425:#len(castellano):
    k, persona = castellano[i]
    #url="https://www.scopus.com/authid/detail.uri?authorId={}".format(k)
    #firefox.get(url)
    ActionChains(chrome).move_to_element(redactar).click(redactar).perform()
    time.sleep(1)
    #try:i
    #apellido, nombre = firefox.find_element(By.XPATH,"//h1[@data-testid='author-profile-name']").text.split(", ")
    #except:
    #nombre = persona["nombre"]
    #apellido = ""
    apellidoNombre = persona["nombre"].split(", ")
    apellido, nombre = apellidoNombre if len(apellidoNombre)==2 else (persona["nombre"], "")
    cantidad_papers = len(persona["papers"])
    #print(i, ",", k, ",", apellido, ",", nombre, ",", cantidad_papers, ",", persona["nombre"])
    print(i, ",", k, ",", cantidad_papers, ",", persona["nombre"])
    mails = list(persona["mails"])
    mails.append("metodosbayesianos@gmail.com")
    input_mail = chrome.find_element(By.XPATH, input_mail_xpath )
    #input_mail.get_attribute("id")
    ActionChains(chrome).move_to_element(input_mail).click(input_mail).perform()
    input_mail.clear()
    input_mail.send_keys(",".join(mails))
    #boton_cc = chrome.find_element(By.XPATH, boton_cc_xpath )
    #ActionChains(chrome).move_to_element(boton_cc).click(boton_cc).perform()
    #input_cc = chrome.find_element(By.XPATH, cc_xpath)
    #input_cc.send_keys("bayesdelsur@gmail.com")
    input_subject = chrome.find_elements(By.XPATH, "//input[@name='subjectbox']")[0]
    input_subject.clear()
    input_subject.send_keys('Bayes Plurinacional')
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








