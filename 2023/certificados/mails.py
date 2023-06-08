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

with open('mails/formulario_de_viaje.txt', 'r') as file:
    # Read the entire contents of the file
    mensaje = file.read()

redactar = chrome.find_elements(By.CLASS_NAME, "z0")[0]
redactar = redactar.find_elements(By.XPATH, ".//div")[0]

#tree = html.fromstring(chrome.page_source)
#e = tree.xpath('//input[@id=":tv"]')[0]
#input_mail_xpath = e.getroottree().getpath(e)
input_mail_xpath = '/html/body/div[25]/div/div/div/div[1]/div[2]/div[1]/div[1]/div/div/div/div[3]/div/div/div[4]/table/tbody/tr/td[2]/form/div[1]/table/tbody/tr[1]/td[2]/div/div/div[1]/div/div[3]/div/div/div/div/div/input'
#tree = html.fromstring(chrome.page_source)
#e = tree.xpath('//div[@id=":r7"]')[0]
#input_texto_xpath = e.getroottree().getpath(e)
input_texto_xpath = '/html/body/div[25]/div/div/div/div[1]/div[2]/div[1]/div[1]/div/div/div/div[3]/div/div/div[4]/table/tbody/tr/td[2]/table/tbody/tr[1]/td/div/div[1]/div[2]/div[3]/div/table/tbody/tr/td[2]/div[2]/div'
#tree = html.fromstring(chrome.page_source)
#e = tree.xpath('//img[@id=":mz"]')[0]
#close_input_xpath = e.getroottree().getpath(e)
close_input_xpath = '/html/body/div[25]/div/div/div/div[1]/div[2]/div[1]/div[1]/div/div/div/div[2]/div/div[2]/div/div/div/div/table/tbody/tr/td[2]/img[3]'
#tree = html.fromstring(chrome.page_source)
#e = tree.xpath('//div[@id=":po"]')[0]
#enviar_xpath = e.getroottree().getpath(e)
enviar_xpath = '/html/body/div[25]/div/div/div/div[1]/div[2]/div[1]/div[1]/div/div/div/div[3]/div/div/div[4]/table/tbody/tr/td[2]/table/tbody/tr[2]/td/div/div/div[4]/table/tbody/tr/td[1]/div/div[2]/div[1]'


data = pd.read_csv("Posters.csv", sep=",")


for i in range(3,data.shape[0]):#i=3
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








