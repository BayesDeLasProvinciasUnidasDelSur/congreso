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

data = pd.read_csv("detalles_mas.csv", sep="|")

data[data["bayes"]>0.0].iloc[0,:]

driver = webdriver.Firefox()
i = 0
for index, persona in data[data["bayes"]>0.0].iterrows():#index=0
    i +=1
    if i in [124]:
        numero = data["Numero"][index]
        nombre = data["Nombre"][index]
        apellido = "-".join(nombre.split("\xa0")[0].split(" "))
        apellido_texto = " ".join(nombre.split("\xa0")[0].split(" "))
        nombre = " ".join(nombre.split("\xa0")[1].split(" ")).title()

        print(index, apellido, numero)
        url = 'https://www.conicet.gov.ar/new_scp/mail.php?id={}&detalle=yes&esprimera=1'.format(numero)
        driver.get(url)

        url_carta = 'http://bayesdelsur.com.ar/invitaciones/{}-{}.pdf'.format(numero, unidecode(apellido))
        print(i, url_carta)

        imagen = driver.find_element(By.XPATH, "//td[@class='general_texto']/img").get_attribute("src")
        clave = imagen.split("k=")[1]

        input_0=driver.find_element(by=By.NAME, value= 'remitente')
        input_0.clear()
        input_0.send_keys('Comisión organizadora del Congreso Bayesiano Plurinacional')
        input_1=driver.find_element(by=By.NAME, value= 'de_mail')
        input_1.clear()
        input_1.send_keys('bayesdelsur@gmail.com')
        input_2=driver.find_element(by=By.NAME, value= 'subject')
        input_2.clear()
        input_2.send_keys('Invitación especial')
        input_3=driver.find_element(by=By.NAME, value= 'message')
        input_3.clear()
        input_3.send_keys('{} {},\n\nUn grupo de investigadores de diferentes regiones del país, reunidos en torno a la aplicación del enfoque bayesiano de la teoría probabilidad, nos dirigimos a usted para invitarle personalmente a participar, activa o pasivamente, de la organización del primer Congreso Bayesiano Plurinacional, a realizarse los días 4 y 5 de agosto del año 2023 en las instalaciones del NODO tecnológico de Santiago del Estero, Argentina.\n\nSi bien la aplicación estricta de las reglas de la probabilidad (enfoque bayesiano) ha mostrado ser la lógica ideal en contextos de incertidumbre, su adopción se vio históricamente limitada debido al costo computacional asociado a la evaluación completa del espacio de hipótesis. Luego de superados estos obstáculos, gracias al crecimiento en la capacidad de cómputo y el desarrollo de métodos eficientes de aproximación, la inercia histórica es ahora su limitación principal.\n\nEl Congreso tiene por objetivo hacer crecer las comunidades bayesianas en Argentina y la Región, reuniendo a estudiantes, docentes, investigadores, emprendedores, practicantes que utilizan, desarrollan o implementan métodos bayesianos en sus respectivos trabajos. Entre los tópicos a tratar se incluye: modelado probabilístico, razonamiento causal, toma de decisiones, programación probabilística, teoría de la información, inteligencia artificial, ciencia de datos, epistemología y metodología, estadística aplicada, pedagogía de la probabilidad, entre otros.\n\nEl apoyo a la organización del Congreso pueden ser: simbólico, ofreciendo su nombre como aval; activo, participando de alguna tarea; o en especies, aportando bienes o dinero. Puede indicar el tipo de participación completando el siguiente formulario: https://bit.ly/apoyo_cbp . La primera circular informativa se encuentra disponible en el sitio bayesdelsur.com.ar\n\nPuede encontrar su invitación personal en el siguiente link: {}\n\nSin otro particular, le saluda a usted muy atentamente la Comisión organizadora del Congreso Bayesiano Plurinacional.\n\nDr MARTIN, Osvaldo. Dr. DÍAZ, Rodrigo. Lic. SERRANO, María Gimena. Lic. LANDFRIED, Gustavo.'.format(apellido_texto,nombre,url_carta))
        input_4=driver.find_element(by=By.NAME, value= 'tmptxt')
        input_4.clear()
        input_4.send_keys(clave)

        enviar=driver.find_element(by=By.CLASS_NAME, value= 'enviar_mail_imagen')
        ActionChains(driver).move_to_element(enviar).click(enviar).perform()
        enviar.click()

        time.sleep(2)
        text = driver.find_element(By.XPATH, "//div[@id='main']").text
        print(text)
        os.system("echo '{}|{}|{}|{}' >> envios.log".format(index, apellido, numero,text))
