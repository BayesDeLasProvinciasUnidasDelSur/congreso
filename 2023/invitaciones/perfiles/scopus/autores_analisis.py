import pickle
import networkx as nx
import csv
import pandas as pd
from collections import defaultdict
import re
import time
import os
import matplotlib.pyplot as plt
import itertools

# DOI metadata
# https://search.crossref.org/

with open('autores_datos.pickle', 'rb') as handle:
    datos = pickle.load(handle)

with open('papers_datos.pickle', 'rb') as handle:
    papers = pickle.load(handle)

k_ejemplo_paper = ('56389488100', 'Organization, evolution and transcriptional profile of hexamerin genes of the parasitic wasp Nasonia vitripennis (Hymenoptera: Pteromalidae)')

def nodos_ejes(pais):
    nodos = [ k for k in datos if pais in datos[k]["paises"]]
    ejes= [ [c for c in itertools.combinations(
set(papers[k]["autores"]).intersection(nodos), 2) ] for k in papers]
    ejes= [e for xs in ejes for e in xs]
    return nodos, ejes



paises = ['Argentina', 'Uruguay', 'Chile', 'Paraguay', 'Bolivia, Plurinational State of', 'Peru', 'Colombia', 'Ecuador', 'Venezuela, Bolivarian Republic of', 'Cuba',  'Mexico', 'Brazil', 'Nicaragua', 'Honduras', 'Guatemala']
autores_por_pais = {  p: sum([1 for k in datos if p in datos[k]["paises"] ])  for p in paises }
autores_por_pais

sorted(autores_por_pais)

NODOS_EJES = { p: nodos_ejes(p) for p in paises  }

Gs = []
for p in paises:
    plt.close()
    Gs.append(nx.Graph())
    Gs[-1].add_nodes_from(NODOS_EJES[p][0])
    Gs[-1].add_edges_from(NODOS_EJES[p][1])
    nx.draw(Gs[-1], node_size = 10)
    plt.savefig("figuras/{}.pdf".format(p),bbox_inches='tight')
    plt.close()




{ p:[c.number_of_nodes()/G.number_of_nodes() for c in sorted(nx.connected_components(G), key=len, reverse=True)][0:2] for G,p in zip(Gs, paises) if len(G) > 0 }



set([q for k in papers for q in papers[k]])
set([q for k in datos for q in datos [k]])


[k for k in papers]


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

sum([len(datos[k]["papers"])>1 for k in datos])



autores_con_contacto_por_pais = {  p: sum([1 for k in datos if (p in datos[k]["paises"]) and len(datos[k]["mails"])>0 ])  for p in paises }
autores_con_contacto_por_pais


[datos[k]["nombre"] for k in datos if ("Argentina" in datos[k]["paises"]) and len(datos[k]["mails"])>0 ]
[(k,datos[k]["nombre"]) for k in datos if ("Argentina" in datos[k]["paises"]) and len(datos[k]["mails"])>0 ]

for k in datos:
    if ("Argentina" in datos[k]["paises"]) and len(datos[k]["mails"])>0 :
        print(datos[k])
        print("")
