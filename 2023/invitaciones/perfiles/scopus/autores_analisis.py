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
from collections import Counter
# DOI metadata
# https://search.crossref.org/


#for k in datos:
    #del datos[k]['mails']
#with open('autores_sin_contacto.pickle', 'wb') as handle:
    #pickle.dump(datos, handle, protocol=pickle.HIGHEST_PROTOCOL)

#Counter(papers.keys()).most_common(10)


with open('autores_datos.pickle', 'rb') as handle:
    datos = pickle.load(handle)

with open('papers_datos.pickle', 'rb') as handle:
    papers = pickle.load(handle)

len(datos)
len(papers)



def ranking_autores_por_papers(top=10,order=2):
    autores_por_papers = [ (datos[k]["nombre"],len(datos[k]["papers"]),sum([1  for p in datos[k]["papers"] if p[0] == 0]),k) for k in datos if "Argentina" in datos[k]["latinos"] ]
    return sorted(autores_por_papers, key=lambda x:x[order], reverse=True)[0:top]

def papers_de(k):
    return [(p, papers[p]["publication_date"]) for p in papers if k in papers[p]["autores"]]


ranking_autores_por_papers(top=10,order=2)


osvaldo_martin = "30567452100"
rodrigo_diaz = "24502677100"
pregliasco = "57211037695"
plastino = "26538012200" # Presidente UNLP 1986-1992
cernuschi_frias = "7003558300" # Fallecido 2021, Decano FIUBA
ciapponi = "24773469000" # Argentino en FIND
# Mujeres del top 20
cuyckens_erica = "55695616600" # 5 (9) Jujuy Estudios Ambientales y Social
carrizo_garcia_carolina = "56178341700" # 4 (5) Cordoba BioVeg
quiroga_paula = "15843952300" # 4 (5) Bariloche
torres_carolina = "57042629400" # 2 (10) BsAs Bacteriología y Virología (IBAVIM)
barboza_gloria = "6701525125" # 0 (10) Cordoba BioVeg


papers_de("6701525125")


Cristian Rodriguez Rivero

autores_por_papers = [ (datos[k]["nombre"],len(datos[k]["papers"]),sum([1  for p in datos[k]["papers"] if p[0] == 0]),k) for k in datos if "Argentina" in datos[k]["latinos"] ]

sorted(autores_por_papers, key=lambda x:x[2], reverse=True)[0:10]

[(p[0]==plastino,p[1], papers[p]["publication_date"]) for p in papers if plastino in papers[p]["autores"]]

[ (p, papers[p]["publication_date"], k) for p in papers for k in papers[p]["autores"] if "Argentina" in datos[k]["latinos"] ][0:-4]

papers[('7101739132', 'MAPAG: a computer program to construct 2- and 3-dimensional antigenic maps')]


[k for k in datos if "Ciapponi" in datos[k]["nombre"]]
kp = [k for k in papers if "24773469000" in papers[k]["autores"]][0]
papers[kp]


set([q for k in datos for q in datos[k]])
set([q for k in papers for q in papers[k]])

datos_para_csv = pd.DataFrame([(int(k), datos[k]["nombre"], "; ".join(datos[k]["paises"]), " | ".join(datos[k]["affil"]), len(datos[k]["papers"]), len(datos[k]["mails"])>0 ) for k in datos ], columns = ["id_persona", "nombre", "paises", "afiliaciones", "papers", "contacto"])
datos_para_csv.to_csv("csv/personas.csv", sep=",")

personasXpapers_para_csv = pd.DataFrame([ (k[0]+"::"+k[1], int(a), [p[0] for p in datos[a]["papers"] if p[1] == k[1]][0] ) for k in papers for a in papers[k]["autores"] ], columns = ["id_paper", "id_persona", "posicion"])
personasXpapers_para_csv.to_csv("csv/papersXpersonas.csv")


papers_para_csv = pd.DataFrame([ (k[0]+"::"+k[1],  "".join(papers[k]["DOI"]) , "".join(papers[k]["ISSN"]) , papers[k]["abstract"],  ";".join(papers[k]["palabras"]), papers[k]["publication_date"], papers[k]["document_type"],  papers[k]["source_type"],  papers[k]["journal"],   papers[k]["cited_by"]  ) for k in papers ], columns = ["id_paper", "doi", "issn", "abstract", "palabras", "Año", "documento", "fuente", "revista", "citas"])
papers_para_csv.to_csv("csv/papers.csv")

#Counter([ a for k in datos for a in datos[k]["affil"] if "Argentina" in datos[k]["paises"] ])

"".join([])

#len([ (datos[k]["nombre"],a) for k in datos for a in datos[k]["affil"] if "Argentina" in datos[k]["paises"] and "Facultad de Ciencias Exactas y Naturales, Universidad de Buenos Aires" in a ])




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

sorted(autores_por_pais.items(), key=lambda x:x[1], reverse=True)

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


componentes = { p:[len(c)/len(G) for c in sorted(nx.connected_components(G), key=len, reverse=True)][0:2] for G,p in zip(Gs, paises) if len(G) > 20 }

sorted(componentes.items(), key=lambda x:x[1], reverse=True)

set([q for k in papers for q in papers[k]])
set([q for k in datos for q in datos [k]])


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

mails = {}
for p in paises:
    mails[p] = sum([len(datos[k]["mails"])>0 for k in datos  if (p in datos[k]["latinos"]) ])



sum([len(datos[k]["papers"])>1 for k in datos])



autores_con_contacto_por_pais = {  p: sum([1 for k in datos if (p in datos[k]["paises"]) and len(datos[k]["mails"])>0 ])  for p in paises }
autores_con_contacto_por_pais


[datos[k]["nombre"] for k in datos if ("Argentina" in datos[k]["paises"]) and len(datos[k]["mails"])>0 ]
[(k,datos[k]["nombre"]) for k in datos if ("Argentina" in datos[k]["paises"]) and len(datos[k]["mails"])>0 ]

for k in datos:
    if ("Argentina" in datos[k]["paises"]) and len(datos[k]["mails"])>0 :
        print(datos[k])
        print("")
