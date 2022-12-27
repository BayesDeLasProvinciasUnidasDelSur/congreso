import pickle
import csv
import pandas as pd
from collections import defaultdict
import re
import time
import os

with open('autores_datos.pickle', 'rb') as handle:
    datos = pickle.load(handle)

datos.keys()

i = 0
j = 0
af = 0
for k in datos:
    if len(datos[k]["mails"])==0 and len(datos[k]["latinos"])>0:
        j +=1
        print(datos[k]["latinos"], datos[k]["nombre"], k)
        if len(datos[k]["affil"])>1:
            af+=1
    if len(datos[k]["mails"])>0 and len(datos[k]["latinos"])>0:
        i +=1
        print(datos[k]["latinos"], datos[k]["nombre"], datos[k]["mails"])

i
j
af
