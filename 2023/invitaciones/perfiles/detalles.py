from lxml import html
import requests
import csv
import pandas as pd
from collections import defaultdict

def palabras(r):
    return ("bayes" in r) or ("Bayes" in r) or ("proba" in r) or ("Proba" in r) or ("Monte Carlo" in r) or ("inferencia" in r) or ("Inferencia" in r) or ("Estima" in r) or ("estima" in r) or ("Episte" in r) or ("episte" in r)

perfiles = pd.read_csv("perfiles.csv")

for i in range(len(perfiles)):#i=0
    p = perfiles.iloc[i,:]
    url0 = 'https://www.conicet.gov.ar/new_scp/detalle.php?keywords=&id={}&datos_academicos=yes'.format(p["numero"])
    try:
        page0 = requests.get(url0,timeout=5)
    except:
        continue
    if (page0.status_code == 200):
        tree0 = html.fromstring(page0.text)
        persona = defaultdict(lambda: None)
        persona["Numero"] = p["numero"]
        persona["Nombre"] = tree0.xpath('//div[@class="titulo_nombre"]/text()')[0]
        contenidos = tree0.xpath('//div[@class="contenido_item"]')
        for c in contenidos:#c=contenidos[0]
            label = c.xpath('./div[@class="contenido_label"]/text()')[0]
            persona[label] = " & ".join(c.xpath('./div[@class="contenido_label_info"]/text()'))

        trabajos = []; bayes=0; proba=0; MC=0; inferencia=0; estima=0; episte=0
        for tipo in ["articulos", "libro", "capitulo", "congresos", "inf_tecnico"]:
            url = 'https://www.conicet.gov.ar/new_scp/detalle.php?keywords=&id={}&{}=yes'.format(p["numero"], tipo)
            try:
                page = requests.get(url,timeout=5)
            except:
                pass

            tree = html.fromstring(page.text)
            renglon = tree.xpath('//div[@class="contenido_renglon"]/text()')
            trabajos = trabajos + [ r for r in renglon if palabras(r)]
            bayes += sum([ 1 for r in renglon if ("bayes" in r) or ("Bayes" in r) ])
            proba += sum([ 1 for r in renglon if ("proba" in r) or ("Proba" in r) ])
            MC += sum([ 1 for r in renglon if ("Monte Carlo" in r)])
            inferencia += sum([ 1 for r in renglon if ("inferencia" in r) or ("Inferencia" in r) ])
            estima += sum([ 1 for r in renglon if ("estima" in r) or ("Estima" in r) ])
            episte += sum([ 1 for r in renglon if ("episte" in r) or ("Episte" in r) ])

        with open('detalles_mas.csv','a') as fd:
            fd.write('{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}|{}\n'.format(persona["Numero"], persona["Nombre"], persona['Título/s'], persona['Categoría'], persona['Disciplina científica'], persona['Disciplina desagregada'], persona['Campo de aplicación'], persona['Especialidad'], persona['Tema'], persona['Palabras clave'], persona['Lugar de trabajo'], persona['Director de  : '], persona['Co director de  : '], bayes, proba, MC, inferencia, estima, episte ," & ".join(trabajos) ))

        #columnas = {'Palabras clave en inglés', 'Director de  : ', 'Lugar de trabajo', 'Especialidad', 'Disciplina desagregada', 'Título/s', 'Palabras clave', 'Tema en inglés', 'Tema', 'Disciplina científica', 'Campo de aplicación', 'id', 'Categoría', 'Co director de  : '}

        print(persona)




