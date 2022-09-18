from lxml import html
import requests
import csv
import pandas as pd
from collections import defaultdict
import pandas as pd
import re
import time
import os
from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support.ui import WebDriverWait # available since 2.4.0
import time
from selenium.webdriver.common.by import By
import selenium

data = pd.read_csv("detalles_mas.csv", sep="|")


numero = data["Numero"][578]
nombre = data["Nombre"][578]
apellido = "-".join(nombre.split("\xa0")[0].split(" "))

url = 'https://www.conicet.gov.ar/new_scp/mail.php?id={}&detalle=yes&esprimera=1'.format(numero)

url_carta = 'http://bayesdelsur.com.ar/invitaciones/{}-{}.pdf'.format(numero, apellido)
page_carta = requests.get(url_carta,timeout=5)
assert (page_carta.status_code == 200)

driver = webdriver.Firefox()
driver.get(url)
driver.find_elements(By.XPATH, '//td/img/')
imagen = driver.find_element(By.XPATH, "//td[@class='general_texto']/img").get_attribute("src")
clave = imagen.split("k=")[1]

input_0=driver.find_element(by=By.NAME, value= 'remitente')
input_0.clear()
input_0.send_keys('Comisión Organizadora del Congreso Bayesiano Plurinacional')
input_1=driver.find_element(by=By.NAME, value= 'de_mail')
input_1.clear()
input_1.send_keys('bayesdelsur@gmail.com')
input_2=driver.find_element(by=By.NAME, value= 'subject')
input_2.clear()
input_2.send_keys('Invitación especial')
input_3=driver.find_element(by=By.NAME, value= 'message')
input_3.clear()
input_3.send_keys('{},\n\nUn grupo de investigadores de todo el país, reunidos en torno a la aplicación del enfoque bayesiano de la teoría probabilidad, nos dirigimos a usted para invitarle personalmente a participar, activa o pasivamente, de la organización del Primer Congreso Bayesiano Plurinacional. \n \nEl Congreso tiene por objetivo hacer crecer las comunidades Bayesianas en Argentina y la Región, reuniendo a estudiantes, docentes, investigadores, emprendedores, practicantes que utilizan, desarrollan o implementan métodos Bayesianos en sus respectivos trabajos. \n\nLa participación pueden ser pasiva, a través de un aval de apoyo (completando el siguiente formulario https://forms.gle/Bhoph97NpNPdA7LTA, o activa a través del contacto directo con la organización, enviando un correo a bayesdelsur@gmail.com. \n\nPuede encontrar su invitación personal en el siguiente link: {}\n\n Sin otro particular, le saluda a usted muy atentamente la comisión organizadora del Congreso Bayesiano Plurinacional. \n\n- Dr. MARTIN, Osvaldo. Investigador Conicet. IMASL-CONICET (San Luis) \n- Dr. Rodrigo Díaz. Investigador Conicet. Universidad Nacional de San Martín. \n- Lic. María Gimena Serrano. Secretaría de Ciencia y Técnica. Gobierno de Santiago del Estero \n- Lic. Gustavo Landfried. Doctorando en Cs de la Computación. Universidad de Buenos Aires'.format(nombre,url_carta))
input_4=driver.find_element(by=By.NAME, value= 'tmptxt')
input_4.clear()
input_4.send_keys(clave)

from selenium.webdriver.common.action_chains import ActionChains
enviar=driver.find_element(by=By.CLASS_NAME, value= 'enviar_mail_imagen')
ActionChains(driver).move_to_element(enviar).click(enviar).perform()
enviar.click()
