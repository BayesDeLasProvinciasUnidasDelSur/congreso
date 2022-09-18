import pandas as pd
import re
import time
import os

data = pd.read_csv("perfiles/detalles_mas.csv", sep="|")

for index, persona in data[data["bayes"]>0.0].iterrows():
    #persona = data.iloc[0,:]
    #LT = ''.join(persona["Lugar de trabajo"].split(" & "))[0:-3]
    #print(LT)
    apellido = "-".join(persona["Nombre"].split("\xa0")[0].split(" "))
    folder = "cartas/{}".format(persona["Numero"])
    if not os.path.exists(folder):
        os.makedirs(folder)
    archivo = "cartas/{}/{}-{}.tex".format(persona["Numero"],persona["Numero"],apellido)
    os.system("cp cartas/carta_modelo.tex {}".format(archivo))
    os.system("sed -i 's/APELLIDO-NOMBRE/{}/g' {}".format(persona["Nombre"], archivo))
    os.system("sed -i 's/CARGO/{}/g' {}".format(persona["Categoría"], archivo))
    os.system("sed -i 's/..\/aux/..\/..\/aux/g' {}".format(archivo))
    os.system("cp cartas/makefile cartas/{}/makefile".format(persona["Numero"]))
    os.system("sed -i 's/carta_modelo/{}-{}/g' cartas/{}/makefile".format(persona["Numero"],apellido, persona["Numero"]))
    os.system("make -C {}".format(folder))
    os.system("cp cartas/{}/{}-{}.pdf cartas/pdf/{}-{}.pdf".format(persona["Numero"],persona["Numero"],apellido,persona["Numero"],apellido))

