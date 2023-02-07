library(igraph)
library(tidygraph)
library(tidyverse)
library(ggraph)
library(visNetwork)
library(htmlwidgets)

# Limpiamos un poco cada dataframe
Per <- read.csv('datos/personas.csv') %>% 
  select(-X) %>% # Borramos X
  rename(id = id_persona) %>% # Cambiamos a nombre generico id
  mutate(id = paste('per',id,sep='_')) %>% # remarcamos que son personas
  mutate(type = TRUE) %>% # Con TRUE identificamos a las personas, util para propiedades bipartitas
  rename(label = nombre) %>% # Ponemos el nombre como label
  mutate(paises = str_remove(paises,'desconocido')) %>% # Borramos el texto "desconocido"
  mutate(paises = str_replace(paises,'; ;|;;',';')) %>%
  mutate(paises = str_remove(paises,'; $|^; ')) %>%
  mutate(afiliaciones = str_trim(str_remove(afiliaciones,'^\\|'))) %>%
  mutate(paises = str_trim(ifelse(paises=='','N/A',paises))) %>%
  mutate(title = paste(
    paste('<b>Author:</b>',label),
    paste('<b>Countries:</b>',paises),
    paste('<b>Affiliations:</b><br>-',gsub('\\|','<br>-',afiliaciones)),
    sep='<br>'
    )) %>%
  mutate(shape = 'dot', # Parámetros gráficos
         color = 'blue')



Pap <- read.csv('datos/papers.csv') %>% 
  select(-X) %>% # Borramos X
  rename(id = id_paper) %>% # Cambiamos a nombre generico id
  mutate(id = paste('pap',id,sep='_')) %>% # Remarcamos que son papers
  unique() %>% # Como hay muchas filas repetidas, nos quedamos con una aparición unica por paper
  mutate(type = FALSE) %>% # Con FALSE identificamos a los papers, util para propiedades bipartitas
  mutate(paper_name = str_remove(id,".*::")) %>% #Nombre del paper
  mutate(label = paste(sub("^(\\S*\\s+\\S+\\s+\\S+\\s+\\S+).*", "\\1",paper_name),'...',sep='')) %>% # Label es nombre acortado del paper
  mutate(title = paste(
    paste('<b>',paper_name,'</b>',sep=''),
    abstract,
    sep='<br><br>')) %>%# titulo es lo que aparece al hacer hover sobre el nodo. Es titulo + abstract
  mutate(shape = 'triangle', # Parámetros gráficos
         color = 'orange')




X <- read.csv('datos/papersXpersonas.csv') %>% 
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

# Retenemos sólo nodos de personas de un país, y borramos lo que quede suelto
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
#pais <- 'Argentina'
dir.create('redes_por_pais')
for(pais in paises_latinoamerica){
  print(paste('Comenzando:',pais))
  gP <- g %>% 
    delete_vertices(v = !grepl(pais,V(g)$paises) & V(g)$type) 
  gP <- gP %>% 
    delete_vertices(degree(gP) == 0) %>%
    as_tbl_graph()
  
  # Visualizaciones de red de personas en formato HTML
  
  # Usamos layour de ggraph
  
  gP$layout <- as.matrix(create_layout(gP,'stress')[,1:2])
  V(gP)$x <- gP$layout[,1]
  V(gP)$y <- -gP$layout[,2]
  print('Red preparada')
  # Generamos la red
  
  visgP <- visIgraph(gP) %>% 
    visInteraction(navigationButtons = TRUE) %>%
    visLegend(addNodes = data.frame(label=c('Author','Paper'),shape=c('dot','triangle'),color=c('blue','orange'),title = 'Nodes'))
  visgP$x$main <- list('text'=pais,style="font-family:Georgia, Times New Roman, Times, serif;font-weight:bold;font-size:20px;text-align:center;")
  visgP$sizingPolicy$browser$fill <- TRUE
  print('Visgraph preparado, guardando...')
  print(visgP)
  
  saveWidget(widget = visgP,sub('XXX',pais,'redes_por_pais/redXXX.html'),selfcontained = FALSE)
  print('Guardado')
  print('--------------------------')
}
