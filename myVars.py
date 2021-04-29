#coding: utf-8
import random
# Semente de aleatoriedade
# random.seed(101010)
RAND_MAX = 2147483647.0
# Para simular o tempo de máquina irei fazer uma pequena manipulacao
# do tempo assumindo segundos como minutos, milisegundos como segundos e etc.
TEMPO_EXPEDIENTE = 43200
CLIENTS_SERVED = 0
TOTAL_CLIENTS = int(random.uniform(300, 320))
print("Expected clients for today:", TOTAL_CLIENTS)

# Variaveis estatisticas
TempoTotalEspera = 0.0
TempoTotalPermanencia = 0.0
TempoTotalSistema = 0.0
TempoTotalServico = 0.0
TotalClientesFila = 0.0
TempoEsperaBloco1 = 0.0
TempoEsperaBloco2 = 0.0
TempoEsperaBloco3 = 0.0
TempoEsperaBloco4 = 0.0


# Definindo quantidade de clients que passam por cada postos_de_atendimento
# e suas caracteristicas
sell_zone_priority_clients = 0.05 * TOTAL_CLIENTS
visiting_clients = 0.2 * TOTAL_CLIENTS
buy_zone_clients = 0.8 * TOTAL_CLIENTS
check_zone_clients = 0.6 * buy_zone_clients
return_zone_clients = 0.05 * check_zone_clients

# Time Blocks
time_block1 = 10800  # type: int # 10-13
time_block2 = 21600  # 13-16
time_block3 = 32400  # ...
time_block4 = 43200

# Time delay Rate
