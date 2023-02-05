# Este script asume que están los archivos descargados en la carpeta datos/

library(igraph)
library(tidygraph)
library(tidyverse)
library(ggraph)

# Cargamos datasets originales
Per <- read.csv('datos/personas.csv')
Pap <- read.csv('datos/papers.csv')
X <- read.csv('datos/papersXpersonas.csv')

# Limpiamos un poco cada dataframe
Per <- Per %>% 
  select(-X) %>% # Borramos X
  rename(id = id_persona) %>% # Cambiamos a nombre generico id
  mutate(id = paste('per',id,sep='_')) %>% # remarcamos que son personas
  mutate(type = TRUE) # Con TRUE identificamos a las personas, util para propiedades bipartitas

Pap <- Pap %>% 
  select(-X) %>% # Borramos X
  rename(id = id_paper) %>% # Cambiamos a nombre generico id
  mutate(id = paste('pap',id,sep='_')) %>% # Remarcamos que son papers
  unique() %>% # Como hay muchas filas repetidas, nos quedamos con una aparición unica por paper
  mutate(type = FALSE) # Con FALSE identificamos a los papers, util para propiedades bipartitas



X <- X %>% 
  select(-X) %>% # Borramos X
  rename(id1 = id_persona ) %>% # Ponemos nombres genericos
  mutate(id1 = paste('per',id1,sep='_')) %>%
  rename(id2 = id_paper ) %>%
  mutate(id2 = paste('pap',id2,sep='_'))

# Armamos dataframes para cada variable
edges <- X
nodes <- bind_rows(Per,Pap)
rm(list = setdiff(ls(),c('edges','nodes')))

# Armamos grafo
g <- graph_from_data_frame(edges,FALSE,nodes) %>% as_tbl_graph()
# Proyección a personas

gPer <- g %>%
  bipartite.projection(which = TRUE) %>%
  as_tbl_graph()

# Proyección a papers

gPap <- g %>%
  bipartite.projection(which = FALSE) %>%
  as_tbl_graph()

# Armamos una función para retener la red formada por autores de un país. 

gen_red_de_pais <- function(g,paises,full=FALSE){
  # g es la red general
  # pais es un vector con paises de interes
  # si full es FALSE, se retienen todos los autores que pertenecen a pais, y sus publicaciones. Si full = TRUE, ademas, se retienen los coautores de estos, sean del origen que sean
  paises_st <- paste(paises,collapse='|')
  g <- g %>% 
    as_tbl_graph() %>%
    activate(nodes) %>%
    filter(
      type == FALSE | (
        paises %>% str_detect(paises_st) 
      )
    )  
  g %>% 
    filter(degree(g)>0) %>%
    return()
}

# Algunos resumenes por pais

paises_todos <- g %>% activate(nodes) %>% as_tibble() %>% select(paises) %>% unlist %>% unique %>% str_split('; ') %>% unlist %>% unique %>% setdiff(NA) %>% sort

paises_latinoamerica <- c('Argentina',
                          'Brazil',
                          'Peru',
                          'Bolivia',
                          'Mexico',
                          'Chile',
                          'Uruguay',
                          'Paraguay',
                          'Venezuela',
                          'Ecuador',
                          'Belize',
                          'Costa Rica',
                          'Cuba',
                          'Colombia',
                          'Dominican Republic',
                          'El Salvador',
                          'Guatemala',
                          'Honduras',
                          'Jamaica',
                          'Nicaragua')

resumen_paises <- lapply(paises_latinoamerica,function(pai){
  gpai <- g %>% gen_red_de_pais(pai)
  tb <- tibble('Country'=pai)
  tb <- bind_cols(
    tb,
    gpai %>% activate(nodes) %>% as_tibble() %>% summarise('nauthor' = sum(type),'npapers'=sum(!type))
  )
  gpai_Per <- gpai %>%
    bipartite.projection(which = TRUE) %>%
    as_tbl_graph()
  tb$mean_papers_per_autor <- mean(degree(gpai,V(gpai)$type))
  tb$mean_coautores <- mean(degree(gpai_Per))
  
  gpai_Pap <- gpai %>%
    bipartite.projection(which = FALSE) %>%
    as_tbl_graph()
  
  
  tb$mean_autores_per_paper <- mean(degree(gpai,!V(gpai)$type))
  
  tb$mean_clustering_autores <- gpai_Per %>% transitivity('global') %>% mean(na.rm=TRUE)
  
  tb$clusters <- clusters(gpai)$no
  tb$bcc_autor_net <- max(clusters(gpai_Per)$csize)
  tb$bcc_pap_net <- max(clusters(gpai_Pap)$csize)
  tb$bcc_full_net <- max(clusters(gpai)$csize)
  tb$autor_mas_papers <- names(which.max(strength(gpai_Per)))
  tb$autor_mas_papers_npapers <- max(strength(gpai_Per))
  tb$autor_mas_coautores_ncoautores <- max(degree(gpai_Per))
  return(tb)
  
}) %>% bind_rows()

resumen_paises %>% View

write.csv(resumen_paises,'resumen_paises.csv',row.names=FALSE)

resumen_paises %>% glimpse

pdf('resumen_paises.pdf')
resumen_paises %>%
  ggplot(aes(y = reorder(Country,npapers), x = npapers)) +
  geom_bar(stat='identity') +
  scale_x_log10(name ='Papers') + 
  scale_y_discrete('') %>% print()

resumen_paises %>%
  ggplot(aes(y = reorder(Country,npapers), x = nauthor)) +
  geom_bar(stat='identity') +
  scale_x_log10(name ='Autores') + 
    scale_y_discrete('') %>% print()

resumen_paises %>%
  ggplot(aes(y = reorder(Country,npapers), x = mean_papers_per_autor)) +
  geom_point() +
  scale_x_log10(name ='Papers por autor') + 
  scale_y_discrete('') %>% print()

resumen_paises %>%
  ggplot(aes(y = reorder(Country,npapers), x = mean_autores_per_paper)) +
  geom_point() +
  scale_x_log10(name ='Autores por paper') + 
  scale_y_discrete('') %>% print()

resumen_paises %>%
  ggplot(aes(y = reorder(Country,npapers), x = bcc_autor_net)) +
  geom_point() +
  scale_x_log10(name ='Máximo grupo de autores') + 
  scale_y_discrete('') %>% print()

resumen_paises %>%
  ggplot(aes(y = reorder(Country,npapers), x = bcc_pap_net)) +
  geom_point() +
  scale_x_log10(name ='Máximo grupo de papers') + 
  scale_y_discrete('') %>% print()

resumen_paises %>%
  mutate(s = bcc_pap_net/npapers) %>%
  ggplot(aes(y = reorder(Country,npapers), x = s)) +
  geom_point() +
  scale_x_log10(name ='Fracción de papers en el máximo grupo') + 
  scale_y_discrete('') %>% print()


resumen_paises %>%
  mutate(s = bcc_autor_net/nauthor) %>%
  ggplot(aes(y = reorder(Country,npapers), x = s)) +
  geom_point() +
  scale_x_log10(name ='Fracción de autores en el grupo máximo') + 
  scale_y_discrete('') %>% print()


resumen_paises %>%
  mutate(sa = bcc_autor_net) %>%
  mutate(sp = bcc_pap_net) %>%
  ggplot(aes(x = sa, y =sp)) +
  geom_point() +
  scale_x_log10(name ='Autores en el grupo máximo') + 
  scale_y_log10(name ='Papers en el grupo máximo')  %>% print()

resumen_paises %>%
  ggplot(aes(y = reorder(Country,npapers), x = mean_clustering_autores)) +
  geom_point() +
  scale_x_log10(name ='Coeficiente de clustering autores') + 
  scale_y_discrete('') %>% print()

resumen_paises %>%
  ggplot(aes(x = mean_clustering_autores, y =npapers)) +
  geom_point() +
  scale_x_continuous(name ='Clustering de autores') + 
  scale_y_log10(name ='Papers') %>% print()
dev.off()