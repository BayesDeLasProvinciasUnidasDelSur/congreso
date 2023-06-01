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


chrome = uc.Chrome(version_main=114)
chrome.get("https://www.google.com/gmail/about/")

# Upgrade chrome
# wget https://dl.google.com/linux/direct/google-chrome-stable_current_amd64.deb
# sudo dpkg -i google-chrome-stable_current_amd64.deb
# Upgrade chromedriver
# version=$(curl -s "https://chromedriver.storage.googleapis.com/LATEST_RELEASE")
# wget -qP /tmp/ "https://chromedriver.storage.googleapis.com/${version}/chromedriver_linux64.zip"
# sudo unzip -o /tmp/chromedriver_linux64.zip -d /usr/bin
# sudo chmod 755 /usr/bin/chromedriver
# chromedriver --version

######################################
######################################
######################################


mensaje = """Buenas {} {},

La invitación para presentar un póster en el Congreso Bayesiano Plurinacional se encuentra disponible en nuestra página web oficial. Puede descargarla a través del siguiente link: http://bayesdelsur.com.ar/invitaciones/posters2023/{}{}.pdf. En la viñeta http://bayesdelsur.com.ar/poster.html encontrará algunas recomendaciones para su elaboración.

Le pedimos que responda este correo confirmando si participará de forma presencial en el congreso. Por cuestiones de organización, le pedimos además que nos envíe un número de teléfono donde podamos ponernos en contacto con usted.

Con el fin de organizar su viaje le recomendamos participar del grupo "Congreso" de la comunidad de whatsapp Bayes Plurinacional https://chat.whatsapp.com/B4wjB4W68wBBcKx3Q16Oxc. Además, le recomendamos participar del grupo de correos electrónicos https://groups.google.com/g/bayes-plurinacional/.

El objetivo durante el Congreso es crear un entorno de confianza favorable para el intercambio y el bienestar. Luego del Congreso, el objetivo es darle estructura a la Comunidad, asignando roles y mecanismos de cambio, para que pueda desarrollarse y funcionar de manera autónoma y descentralizada. Los seminarios virtuales se realizarán de forma permanente con el objetivo de crear puentes al interior de la Comunidad, transmitiendo a un público lo más amplio posible la flexibilidad y la potencia del enfoque bayesiano.

Atentamente,
Comisión organizadora del Congreso Bayesiano Plurinacional 2023.

Redes sociales.
- Página web oficial: https://bayesdelsur.com.ar
- Linkedin: https://www.linkedin.com/company/bayes-plurinacional/
- Twitter: https://twitter.com/BayesDelSur
- Mastodon: https://bayes.club/@BayesDelSur
- Youtube: https://www.youtube.com/@bayesdelsur
"""


redactar = chrome.find_elements(By.CLASS_NAME, "z0")[0]
redactar = redactar.find_elements(By.XPATH, ".//div")[0]

#tree = html.fromstring(chrome.page_source)
#e = tree.xpath('//input[@id=":tv"]')[0]
#input_mail_xpath = e.getroottree().getpath(e)
input_mail_xpath = '/html/body/div[24]/div/div/div/div[1]/div[2]/div[1]/div[1]/div/div/div/div[3]/div/div/div[4]/table/tbody/tr/td[2]/form/div[1]/table/tbody/tr[1]/td[2]/div/div/div[1]/div/div[3]/div/div/div/div/div/input'
#tree = html.fromstring(chrome.page_source)
#e = tree.xpath('//div[@id=":r7"]')[0]
#input_texto_xpath = e.getroottree().getpath(e)
input_texto_xpath = '/html/body/div[24]/div/div/div/div[1]/div[2]/div[1]/div[1]/div/div/div/div[3]/div/div/div[4]/table/tbody/tr/td[2]/table/tbody/tr[1]/td/div/div[1]/div[2]/div[3]/div/table/tbody/tr/td[2]/div[2]/div'
#tree = html.fromstring(chrome.page_source)
#e = tree.xpath('//img[@id=":mz"]')[0]
#close_input_xpath = e.getroottree().getpath(e)
close_input_xpath = '/html/body/div[24]/div/div/div/div[1]/div[2]/div[1]/div[1]/div/div/div/div[2]/div/div[2]/div/div/div/div/table/tbody/tr/td[2]/img[3]'
#tree = html.fromstring(chrome.page_source)
#e = tree.xpath('//div[@id=":po"]')[0]
#enviar_xpath = e.getroottree().getpath(e)
enviar_xpath = '/html/body/div[24]/div/div/div/div[1]/div[2]/div[1]/div[1]/div/div/div/div[3]/div/div/div[4]/table/tbody/tr/td[2]/table/tbody/tr[2]/td/div/div/div[4]/table/tbody/tr/td[1]/div/div[2]/div[1]'


data = pd.read_csv("Posters.csv", sep=",")


for i in range(1,data.shape[0]):
    persona = data.iloc[i,]
    ActionChains(chrome).move_to_element(redactar).click(redactar).perform()
    time.sleep(1)
    nombre = persona["Nombre"]
    apellido = persona["Apellido"]
    nombre_file = unidecode("".join(nombre.split(" ")))
    apellido_file = unidecode("".join(apellido.split(" ")))
    print(nombre, apellido)
    mails = [persona["Correo"]]
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
    input_subject.send_keys('Información personal sobre el Congreso Bayesiano Plurinacional')
    input_texto = chrome.find_element(By.XPATH, input_texto_xpath)
    input_texto.clear()
    input_texto.send_keys(mensaje.format(nombre, apellido, nombre_file, apellido_file))
    enviar = chrome.find_element(By.XPATH, enviar_xpath)
    ActionChains(chrome).move_to_element(enviar).click(enviar).perform()
    time.sleep(1.5)





chrome.close()








