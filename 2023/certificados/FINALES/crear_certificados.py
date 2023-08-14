import pandas as pd
import re
import time
import os
from unidecode import unidecode
import shutil

data = pd.read_csv("ACREDITACIONES.csv", sep=",")


for index, persona in data.iterrows():
    #persona = data.iloc[3,:]
    #LT = ''.join(persona["Lugar de trabajo"].split(" & "))[0:-3]
    #print(LT)
    nombre = persona["Nombre y Apellido"]
    nombre_file = unidecode("".join(nombre.split(" ")))
    os.system("cp certificado.tex certificado_tmp.tex ")
    os.system("sed -i 's/NOMBRE/{}/g' certificado_tmp.tex".format(nombre))
    charla = persona["Charla"]
    poster = persona["Poster"]
    if charla:
        titulo = "exponente de una charla"
    if poster:
        titulo = "exponente de un póster"
    if (not charla) and (not poster):
        titulo = "oyente"
    os.system("sed -i 's/ROL/{}/g' certificado_tmp.tex".format(titulo))
    os.system("pdflatex certificado_tmp.tex")
    os.system("mv certificado_tmp.pdf pdf/{}.pdf".format(nombre_file))


