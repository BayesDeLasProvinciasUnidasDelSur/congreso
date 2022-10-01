import pandas as pd
import re
import time
import os
from unidecode import unidecode

data = pd.read_csv("perfiles/detalles_mas.csv", sep="|")

for index, persona in data[data["bayes"]>0.0].iterrows():
    #persona = data.iloc[0,:]
    #LT = ''.join(persona["Lugar de trabajo"].split(" & "))[0:-3]
    #print(LT)
    nombre = " ".join(persona["Nombre"].split("\xa0")[1].split(" ")).title()
    apellido = "-".join(persona["Nombre"].split("\xa0")[0].split(" "))
    apellido_texto = "-".join(persona["Nombre"].split("\xa0")[0].split(" "))
    folder = "cartas/{}".format(persona["Numero"])
    if not os.path.exists(folder):
        os.makedirs(folder)
    archivo = "cartas/{}/{}-{}.tex".format(persona["Numero"],persona["Numero"],unidecode(apellido))
    os.system("cp cartas/carta_modelo.tex {}".format(archivo))
    os.system("sed -i 's/APELLIDO-NOMBRE/{} {}/g' {}".format(apellido_texto, nombre, archivo))
    os.system("sed -i 's/CARGO/{}/g' {}".format(persona["Categoría"], archivo))
    os.system("sed -i 's/..\/aux/..\/..\/aux/g' {}".format(archivo))
    os.system("cp cartas/makefile cartas/{}/makefile".format(persona["Numero"]))
    os.system("sed -i 's/carta_modelo/{}-{}/g' cartas/{}/makefile".format(persona["Numero"],unidecode(apellido), persona["Numero"]))
    os.system("make -C {}".format(folder))
    os.system("cp cartas/{}/{}-{}.pdf cartas/pdf/{}-{}.pdf".format(persona["Numero"],persona["Numero"],unidecode(apellido),persona["Numero"],unidecode(apellido)))

