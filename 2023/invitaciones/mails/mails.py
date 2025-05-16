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




ingles = """Hi {} {},

The Plurinational Bayes community, with the support of Externado University of Colombia, invites you to the event Plurinational Bayes BOGOTÁ 2025 "Plural Intelligence", taking place from October 15 to 17, focused on optimal decision-making under uncertainty grounded in the Bayesian approach of artificial intelligence and machine learning (the approximation to the strict application of probability rules).

- Web of the event: https://bayesplurinacional.org

The event will include keynote talks and hands-on workshops led by leading experts in Bayesian Inference, Artificial Inteligence, and Machine Learning. Confirmed speakers include Mariano Gabitto (recipient of the 2021 International Society for Bayesian Analysis award), Cathy O’Neil (author of Weapons of Math Destruction), Gavino Puggioni, and six outstanding young Latin American researchers trained under mentors such as Kevin Murphy, Michael Elad, Aapo Hyvärinen, and Felipe Tobar among others.

The call for poster and academic presentation proposals is open until June 15. To apply, please submit the title and a short abstract of your work via the appropriate form:

- Form: https://forms.gle/XmHc3DHT3KzeHmEh8

If your proposal is accepted, you will be asked to submit a PDF of your extended abstract (maximum two pages) or your poster (vertical A0 format) as name-surname.pdf to admin@bayesplural.org, with a copy to investigacioncienciadedatos@uexternado.edu.co.

If you want just to attend the activities of the event (lectures, workshops, presentations, and others) you must be pre-register at

- Pre-registration: https://landing.uexternado.edu.co/mat-meetup-bayes-y-ml

Participants who have taken part in previous Plurinational Bayes activities will be exempt from the registration fee. Scholarships will be available for accepted works.

Best Regards.
Plurinational Bayes.

Optimal beliefs distributions given the available information. Intersubjective agreement in context of uncertainty.
"""

portugues = """Olá {} {},

A comunidade Plurinacional Bayes, com o apoio da Universidade Externado da Colômbia, convida você para o evento Plurinacional Bayes BOGOTÁ 2025 "Inteligência Plural", que será realizado de 15 a 17 de outubro, com foco na tomada de decisões ótimas sob incerteza, com base na abordagem bayesiana de inteligência artificial e aprendizado de máquina (a aproximação à aplicação estrita das regras de probabilidade).

- Site do evento: https://bayesplurinacional.org

O evento incluirá palestras e workshops práticos conduzidos pelos renomados especialistas em Inferência Bayesiana, Inteligência Artificial e Aprendizado de Máquina. Entre os palestrantes confirmados estão Mariano Gabitto (ganhador do prêmio da Sociedade Internacional de Análise Bayesiana de 2021), Cathy O'Neil (autora de Weapons of Math Destruction), Gavino Puggioni e seis jovens pesquisadores latino-americanos de destaque, treinados por mentores como Kevin Murphy, Michael Elad, Aapo Hyvärinen e Felipe Tobar, entre outros.

A chamada para propostas de pôsteres e apresentações acadêmicas está aberta até 15 de junho. Para se inscrever, envie o título e um breve resumo de seu trabalho por meio do formulário apropriado (aceitam-se trabalhos em português):

- Formulário: https://forms.gle/XmHc3DHT3KzeHmEh8

Se a sua proposta for aceita, você deverá enviar um PDF do seu resumo estendido (máximo de duas páginas) ou do seu pôster (formato A0 vertical) como nome-sobrenome.pdf para admin@bayesplural.org, com uma cópia para investigacioncienciadedatos@uexternado.edu.co.

Se quiser apenas participar das atividades do evento (palestras, workshops, apresentações e outros), você deverá fazer a pré-inscrição em

- Pré-inscrição: https://landing.uexternado.edu.co/mat-meetup-bayes-y-ml

Participantes que já participaram de atividades anteriores do Bayes Plurinacional estarão isentos da taxa de inscrição. Bolsas estarão disponíveis para trabalhos aceitos.

Atenciosamente,
Bayes Plurinacional.

Distribuição de crenças ótimas dadas as informações disponíveis. Acordo intersubjetivo em contextos de incerteza.
"""

espanol = """Buen día {} {},

La comunidad Bayes Plurinacional, con el apoyo de la Universidad Externado de Colombia, invita al evento presencial Bayes Plurinacional BOGOTÁ 2025 "Inteligencia Plural", que se llevará a cabo del 15 al 17 de octubre de 2025. Este evento está dedicado a la toma óptima de decisiones bajo incertidumbre, basada en el enfoque bayesiano de la inteligencia artificial y el aprendizaje automático (aproximación a la aplicación estricta de las reglas de la probabilidad).

- Página web del evento: https://bayesplurinacional.org

El evento contará con conferencias magistrales y talleres prácticos impartidos por reconocidos expertos en inferencia bayesiana, inteligencia artificial y aprendizaje automático, entre los que se encuentran Mariano Gabitto (ganador del premio 2021 de la International Society for Bayesian Analysis), Cathy O’Neil (autora de Weapons of Math Destruction), Gavino Puggioni y seis destacados jóvenes investigadores latinoamericanos formados por Kevin Murphy, Michael Elad, Aapo Hyvärinen, Felipe Tobar entre otros.

La convocatoria para la presentación de pósteres y trabajos académicos está abierta hasta el 15 junio. Para postularse, por favor envíe el título y un breve resumen de su trabajo a través del siguiente formulario:

- Presentación de trabajos: https://forms.gle/dfKb9fJ8HQ5xkg7k7

En caso de que su propuesta sea aceptada, se le solicitará posteriormente el envío del PDF con su resumen extendido (máximo dos páginas) o su póster (formato vertical A0) con el formato "nombre-apellido.pdf" al correo admin@bayesplural.org, con copia a investigacioncienciadedatos@uexternado.edu.co.

Quienes solo deseen asistir a las actividades del evento (conferencias, talleres, presentaciones y otras), deberán registrarse en el siguiente link

- Inscripción para participar del evento: https://landing.uexternado.edu.co/mat-meetup-bayes-y-ml

Quienes hayan participado en alguna actividad previa de Bayes Plurinacional no deberán pagar la cuota de inscripción. Habrá becas disponibles para ponentes y presentadores de pósteres aceptados que requieran apoyo económico.

Atentamente,
Bayes Plurinacional

Distribución de creencias óptimas dada la información disponible.
Acuerdos intersubjetivos en contextos de incertidumbre.
"""



mensaje = espanol

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
    return sorted([(k,datos[k]) for k in datos if (len(datos[k]['mails'])>0) and (len(datos[k]['latinos'])>0) and not ("Brazil" in datos[k]['latinos']) ],key=lambda x: x[0])

castellano = personas()

#len(castellano)
#np.where(['Neme, Gustavo' == persona[1]["nombre"] for persona in castellano ])


#set([q for k in datos for q in datos[k]])
i =  882;
no_enviados = []
maximo = i + 500
repeticiones = 0
while repeticiones <=2:
    j=0
    while j < 4 and i < min(maximo, len(castellano)):
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
            input_cc.send_keys("gustavolandfried@gmail.com, admin@bayesplural.org")
            input_subject = chrome.find_elements(By.XPATH, "//input[@name='subjectbox']")[0]
            input_subject.clear()
            input_subject.send_keys('Plurinational Bayes BOGOTÁ 2025')
            input_texto = chrome.find_element(By.XPATH, input_texto_xpath)
            input_texto.clear()
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
    repeticiones += 1
    time.sleep(360)

sound.play()



chrome.close()








