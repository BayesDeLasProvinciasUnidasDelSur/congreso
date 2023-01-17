library(igraph)
library(tidygraph)
library(tidyverse)
library(ggraph)
library(visNetwork)
library(htmlwidgets)

#setwd("~/meta/membership/bayes/congreso/comunidad/red/scopus")

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

# Retenemos sólo nodos de personas de Argentina, y borramos lo que quede suelto

gArg <- g %>% 
  delete_vertices(v = !grepl('Argentina',V(g)$paises) & V(g)$type) 
gArg <- gArg %>% 
  delete_vertices(degree(gArg) == 0) %>%
  as_tbl_graph()

# Primer grafiquin

gArg %>% 
  activate(nodes) %>%
  mutate(type = ifelse(type,'Autor','Paper')) %>%
  ggraph() +
  geom_edge_link() +
  geom_node_circle(aes(fill=type,r=.25)) +
  theme_graph() +
  scale_fill_discrete(name = 'Color')

visIgraph(gArg)
saveWidget(visIgraph(gArg), file="red.html") # selfconteiner

cArg <- components(gArg, mode = c("weak", "strong"))

g_i = induced_subgraph(gArg, cArg$membership==which.max(cArg$csize))



g_i %>%
  as_tbl_graph() %>%
  activate(nodes) %>%
  mutate(type = ifelse(type,'Autor','Paper')) %>%
  ggraph() +
  geom_edge_link() +
  geom_node_label(aes(label=nombre,fill=type,r=.25)) +
  theme_graph() +
  scale_fill_discrete(name = 'Color')


g_i %>%
  as_tbl_graph() %>%
  activate(nodes) %>%
  mutate(type = ifelse(type,'Autor','Paper')) %>%
  ggraph() +
  geom_edge_link() +
  geom_node_label(aes(label=nombre,fill=type,r=.25)) +
  theme_graph() +
  scale_fill_discrete(name = 'Color')

g_i %>%
  as_tbl_graph() %>%
  activate(nodes) %>%
  mutate(type = ifelse(type,'Autor','Paper')) %>%
  ggraph() +
  geom_edge_link() +
  geom_node_circle(aes(fill=type,r=.25)) +
  theme_graph() +
  scale_fill_discrete(name = 'Color')


