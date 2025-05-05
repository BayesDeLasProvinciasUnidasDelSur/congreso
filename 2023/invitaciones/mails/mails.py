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


mensaje = """Hi {} {},

The Plurinational Bayes community, with the support of the Department of Mathematics at Universidad Externado de Colombia, invites you to the event Plurinational Bayes BOGOTÁ 2025 "Plural Intelligence," taking place from October 15 to 17. The event is dedicated to optimal decision-making under uncertainty using the Bayesian approach to artificial intelligence and machine learning (an approximation to the strict application of the rules of probability).

The event will feature keynote lectures and hands-on workshops delivered by leading experts [1] in Bayesian inference, artificial intelligence, and machine learning, including Mariano Gabitto (winner of the 2021 International Society of Bayesian Analysis award), Catherine O’Neil (author of Weapons of Math Destruction), Gavino Puggioni, and six outstanding young Latin American researchers trained under Kevin Murphy, Michael Elad, Aapo Hyvärinen, Felipe Tobar, among others.

The call for poster sessions and academic presentations is open until May 31. To apply, please complete the form

- English version: https://forms.gle/XmHc3DHT3KzeHmEh8
- Spanish version: https://forms.gle/dfKb9fJ8HQ5xkg7k7

with the title and a brief abstract of your work. If your proposal is accepted, you will later be asked to submit either an extended abstract (maximum 2 pages) or the poster (vertical A0 sheet) in a file named name-surname.pdf to admin@bayesplural.org with a copy to investigacioncienciadedatos@uexternado.edu.co.

Those who wish to attend the event to participate in the lectures, workshops, presentations, and other activities must register [2]. Anyone who has participated in any Plurinational Bayes activity or is part of the mailing group [3] (access requests accepted until June 10) will not have to pay the registration fee. Scholarships will be available for approved speakers and poster presenters who require financial assistance.

For more information, please visit https://bayesplurinacional.org .

[1] https://bayesplurinacional.org/_pages/es/2025/disertantes.html
[2] https://landing.uexternado.edu.co/mat-meetup-bayes-y-ml
[3] https://groups.google.com/g/bayes-plurinacional
"""


redactar = chrome.find_elements(By.CLASS_NAME, "z0")[0]
redactar = redactar.find_elements(By.XPATH, ".//div")[0]

# Abrir redactar
tree = html.fromstring(chrome.page_source)
e = tree.xpath('//input[@aria-label="Destinatarios en Para"]')[0]
input_mail_xpath = e.getroottree().getpath(e)
e = tree.xpath('//div[@aria-label="Cuerpo del mensaje"]')[0]
input_texto_xpath = e.getroottree().getpath(e)
e = tree.xpath('//div[@aria-label="Enviar ‪(Ctrl-Enter)‬"]')[0]
enviar_xpath = e.getroottree().getpath(e)
e = tree.xpath('//span[@aria-label="Agregar destinatarios a Cc ‪(Ctrl-Mayús-C)‬"]')[0]
boton_cc_xpath = e.getroottree().getpath(e)

# Abrir CC
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
    return sorted([(k,datos[k]) for k in datos if (len(datos[k]['mails'])>0) and (len(datos[k]['latinos'])>0) and ("Brazil" in datos[k]['latinos']) ],key=lambda x: x[0])

castellano = personas()

#len(castellano)
#np.where(['Cristina, Juan' == persona[1]["nombre"] for persona in castellano ])


#set([q for k in datos for q in datos[k]])
i = 2029;
no_enviados = []
j = 0
maximo = 1530 + 500
while i < 5000 and j < 4 and i < maximo:#3900len(castellano):
    try:
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
        input_cc.send_keys("gustavolandfried@gmail.com, bayesplurinacional@gmail.com")
        input_subject = chrome.find_elements(By.XPATH, "//input[@name='subjectbox']")[0]
        input_subject.clear()
        input_subject.send_keys('Plurinational Bayes BOGOTÁ 2025')
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
        j = 0
        print(i, ",", k, ",", cantidad_papers, ",", persona["nombre"])
    except:
        close_mail = chrome.find_element(By.XPATH, close_input_xpath )
        ActionChains(chrome).move_to_element(close_mail).click(close_mail).perform()
        j = j + 1
        no_enviados.append(i)
        print(i, ",", k, ",", cantidad_papers, ",", persona["nombre"], "NO ENVIADO")
    #
    i = i + 1


sound.play()



chrome.close()








