presupuesto = 220000


gastos_previos = 4500 * 2 + 5000 * 2

# Subsidio departamentos.
# Pagan 8700 por noche. Les cobra solo las noches que durmieron, no las que reservamos. Si en promedio los 7 se quedaron 3 noches entonces:
noche = 8700
pagan = 7500 # Tarifa con subsidio.
subsidio = (noche - pagan)*(4+4+2+2+3)
# CBUs subsidios (X_N por N noches)
RoccoDiTella_X_3 = 'roccodt'
MartinAmigo_X_2 = 'aguja.conde.crudo'
JuanZaragosa_X_2 = 'aguja.conde.crudo'
NicolasAlejandroComay_X_4 = "cactus.abrazo.abaco"
Feole_X_4 = "taxi.romero.vuelo"


# Presupuesto Neto, sin subsidio
presupuesto_neto = presupuesto - subsidio

# Cantidad de becas pedidas (12 anotadas en https://docs.google.com/spreadsheets/d/1sJ5LJ1LufQ8mWdoqhgp1FMsm6G26pb9v/edit#gid=1574989191 + Gonzalo Ríos - Hossein Dinani )
pedidos = 12
por_persona = presupuesto_neto / pedidos

# Ponemos como cota 20 dolares a valor paralelo (550 al 2 de agosto).
por_persona_maximo = 20 * 550

# Efectivo
# Albert Ortiz = 8000
# Gonzalo Ríos = 8000
efectivo =  8000 * 2

# Transferencia por becas
transferencia = 11000 * 10
# CBUs Becas
AnaVeronicaScotta = 0110213230021304190483
AndreaGoijman = 0110581030058105404633
CarlosIguaran = 0720769588000038792818
DiegoSevilla = 0650085602000007580435
JavierArellana = 0070019130004060708864
LucianoMoffatt = 0
LuigginaCappellotto = 0110085330008506153779
MatiasAlejandroVera = 0110003730000308691697
NicolasAlejandroComay = 0110127630012711856583
VictoriaNogues = 0110127630012711857265

# Sobran
saldo = presupuesto_neto - efectivo - transferencia - gastos_previos

Dolar_al_9_agosto_2023 = 710
Reserva_casa_Salta_25_junio_2024 = 130000

A_favor_gustavo = Reserva_casa_Salta_25_junio_2024 - (saldo * (1300/Dolar_al_9_agosto_2023 ))
