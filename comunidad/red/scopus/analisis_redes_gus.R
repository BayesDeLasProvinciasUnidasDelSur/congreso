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

gArgPer <- gArg %>%
  bipartite.projection(which=TRUE) %>%
  as_tbl_graph()

gArgPer %>%
  mutate(fuerza = strength(gArgPer)) %>% 
  ggraph() +
  geom_edge_link() +
  geom_node_circle(aes(fill=fuerza,r=.25)) +
  theme_graph() +
  scale_fill_gradient(name = '#Papers',low = 'blue',high='red') +
  ggtitle('Red Autores')

gArgPer %>%
  mutate(fuerza = strength(gArgPer)) %>% 
  as.data.frame() %>%
  ggplot(aes(x=fuerza)) +
  geom_histogram(binwidth = 1, fill='white',color='black') +
  scale_x_continuous(name='#Papers',breaks = seq(0,80,5)) +
  scale_y_continuous(name='Cantidad de autores',breaks = seq(0,150,10)) +
  geom_vline(aes(xintercept=mean(fuerza)),lwd=1.25,lty='dashed') +
  theme_light() +
  ggtitle('Autores de Argentina')
  
# Algun resumencito de los autores
gArgPer %>%
  mutate(fuerza = strength(gArgPer)) %>% 
  as.data.frame() %>%
  select(fuerza) %>% 
  summary()
  
gArgPer %>%
  mutate(grupo = clusters(gArgPer)$membership) %>%
  as.data.frame() %>%
  group_by(grupo) %>%
  summarize(n = n()) %>%
  ggplot(aes(x=n)) +
  geom_histogram(binwidth = 1) +
  scale_x_continuous(name='Cantidad de autores',breaks = seq(0,80,5)) +
  scale_y_continuous(name='Cantidad de grupos',breaks = seq(0,150,10)) +
  geom_vline(aes(xintercept=mean(n)),lwd=1.25,lty='dashed') +
  theme_light() +
  ggtitle('Autores de Argentina')


gArgPer %>%
  mutate(grupo = clusters(gArgPer)$membership) %>%
  as.data.frame() %>%
  group_by(grupo) %>%
  summarize(n = n()) %>%
  select(n) %>%
  summary()
