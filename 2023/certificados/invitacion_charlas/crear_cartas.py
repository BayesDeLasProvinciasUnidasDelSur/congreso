import pandas as pd
import re
import time
import os
from unidecode import unidecode
import shutil

data = pd.read_csv("../Charlas.csv", sep=",")

for index, persona in data.iterrows():
    #persona = data.iloc[5,:]
    #LT = ''.join(persona["Lugar de trabajo"].split(" & "))[0:-3]
    #print(LT)
    nombre = persona["Nombre"]
    apellido = persona["Apellido"]
    nombre_file = unidecode("".join(nombre.split(" ")))
    apellido_file = unidecode("".join(apellido.split(" ")))
    titulo = persona["Titulo"]
    os.system("cp certificado_invitacion_modelo.tex certificado_invitacion_tmp.tex ")
    os.system("sed -i 's/APELLIDO, NOMBRE/{}, {}/g' certificado_invitacion_tmp.tex".format(apellido, nombre))
    os.system("sed -i 's/TITULO/{}/g' certificado_invitacion_tmp.tex".format(titulo))
    os.system("pdflatex certificado_invitacion_tmp.tex")
    os.system("mv certificado_invitacion_tmp.pdf pdf/{}{}.pdf".format(nombre_file,apellido_file))


