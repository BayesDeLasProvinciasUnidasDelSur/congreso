library(igraph)
library(stringr)
library(dplyr)

personas = read.csv("datos/personas.csv")
papers = read.csv("datos/papers.csv")
papersXpersonas = read.csv("datos/papersXpersonas.csv")



pais <- function(pais){
    return(str_detect(personas[["paises"]], pais) )
}



query = merge(x=papersXpersonas, y=personas, by="id_persona")
query = query[str_detect(query[["paises"]], "Argentina"),c("id_paper", "id_persona")]
query = merge(x=query,y=query,by="id_paper")
query = query[query["id_persona.x"] < query["id_persona.y"], c("id_persona.x","id_persona.y")]
query = query %>% add_count(across(everything()))

nodos_ar <- data.frame(name=personas[pais("Argentina"),"id_persona"],
                     size=personas[pais("Argentina"),"papers"],
                     nombre=personas[pais("Argentina"),"nombre"],
                     afiliaciones=personas[pais("Argentina"),"afiliaciones"])
ejes_ar <- data.frame(from=query["id_persona.x"],
                        to=query["id_persona.y"],
                        friendship=query["n"])

g <- graph_from_data_frame(ejes_ar, directed=FALSE, vertices=nodos_ar)
print(g, e=TRUE, v=TRUE)
