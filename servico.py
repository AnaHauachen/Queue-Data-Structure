from queue import Queue
from threading import  Thread,ThreadError
import random
import time
from functions import *

def AtrasoPorPeriodoDeTempo(now, delay):
    if now >= 0 and now <= time_block1:
        myVars.TempoEsperaBloco1 += delay
    elif now > time_block1 and now <= time_block2:
        myVars.TempoEsperaBloco2 += delay
    elif now > time_block2 and now <= time_block3:
        myVars.TempoEsperaBloco3 += delay
    elif now > time_block3 and now <= time_block4:
        myVars.TempoEsperaBloco4 += delay

class Posto():
    def __init__(self,qty_queues, qty_postos, qty_priority_queues=1):
        self.queues = [Queue() for i in range(qty_queues)] # creates queues
        self.postos = [0 for i in range(qty_postos)] # 0 means free!
        self.qty_priority_queues = qty_priority_queues
        self.isOpen = True
        self.fila_eventos = list()

        #     define priority queues
        for i in range(0, qty_priority_queues):
            self.queues[i].isPriority = True

    def attend(self):
        # put client on queue
        # only one queue exists?
        while self.isOpen:
            if len(self.fila_eventos):
                c = self.fila_eventos[0][0]
                clock = self.fila_eventos[0][1]

                if len(self.queues) == 1:
                    # If only one queue exists then it has to be priority
                    self.queues[0].isPriority = True
                    self.queues[0].put(c)
                    myVars.TotalClientesFila+=1

                    for q in range(0,len(self.postos)):
                        # Ponto de atendimento livre?
                        if not self.postos[q] and self.queues[0].size():
                            # Chamando clientes
                            for i in range(self.queues[0].size()):
                                front = self.queues[0].front()
                                client = self.queues[0].get(front)

                                # Metrics
                                tempo_espera = clock.t - client[1].T0
                                myVars.TempoTotalEspera += tempo_espera
                                AtrasoPorPeriodoDeTempo(clock.t, tempo_espera)

                                # Definindo tempo de servico
                                ts = DeterminarTempoServico(0.5, 2.0, client[1].T0)
                                tempo_espera = ts
                                client[1].delay += tempo_espera

                                # Update clock
                                eventoSaida(client[1], clock)

                                # Coletando metricas
                                myVars.TempoTotalServico+=ts

                                # Atendido
                                self.queues[0].remove(front)
                                # self.fila_eventos.append(client[1])
                                del(self.fila_eventos[0])

                                # NOTE: retornar o no para ser encaminhado para o proximo setor
                                destiny = client[1].destiny
                                if destiny == -1:
                                    client[1].where_am_i = -1
                                elif destiny > client[1].where_am_i:
                                    client[1].where_am_i += 1
                                elif destiny <= client[1].where_am_i:
                                    client[1].where_am_i = -1

                else:
                    while self.isOpen:
                        # do we have clients?
                        if len(self.fila_eventos):
                            c = self.fila_eventos[0][0]
                            clock = self.fila_eventos[0][1]

                            # Look for a minimum queue
                            min_queue_length = 999999
                            min_queue = -1
                            to = len(self.queues)

                            # is a priority client?
                            if c.priority:
                                to = self.qty_priority_queues
                            # Find a minimum queue for this client
                            for q in range(0,to):
                                tam = self.queues[q].size()
                                if tam < min_queue_length:
                                    min_queue_length = tam
                                    min_queue = q

                            self.queues[min_queue].put(c)
                            myVars.TotalClientesFila += 1
                            # is free?
                            if not self.postos[min_queue]:
                                front = self.queues[min_queue].front()
                                client = self.queues[min_queue].get(front)

                                # Metrics
                                tempo_espera = clock.t - client[1].T0
                                myVars.TempoTotalEspera += tempo_espera
                                AtrasoPorPeriodoDeTempo(clock.t, tempo_espera)

                                # Tempo servico
                                ts = DeterminarTempoServico(0.5, 2.0, client[1].T0)
                                tempo_espera = ts
                                client[1].delay += tempo_espera

                                # Update clock
                                eventoSaida(client[1], clock)

                                # Coletando valores
                                myVars.TempoTotalServico+=ts

                            # Remove from queue
                            self.queues[min_queue].remove(front)
                            # self.fila_eventos.append(client[1])
                            del (self.fila_eventos[0])

                            # NOTE: retornar o no para ser encaminhado para o proximo setor
                            destiny = client[1].destiny
                            if destiny == -1:
                                client[1].where_am_i = -1
                            elif destiny > client[1].where_am_i:
                                client[1].where_am_i += 1
                            elif destiny <= client[1].where_am_i:
                                client[1].where_am_i = -1


    def stop(self):
        while len(self.fila_eventos):
            continue
        # self.contadoresEstatisticos()
        self.isOpen = False


class Servico():
    def __init__(self):
        self.isOpen = True
        self.postos = dict()
        self.fila_evento_saida = list()
        # Lista de espera
        self.wait_queue = list()

        # self.tipo = tipo
        # zona de venda
        # if self.tipo == 0:
        self.postos[0] = Posto(1, 10)
        # Zona pagamento
        # elif self.tipo == 1:
        self.postos[1] = Posto(4, 4, 2)
        # zona de levantamento
        # elif self.tipo == 2:
        self.postos[2] = Posto(1, 2)

    #     Iniciando threads para cada setor
        t0 = Thread(None, self.postos[0].attend, None)
        t1 = Thread(None, self.postos[1].attend, None)
        t2 = Thread(None, self.postos[2].attend, None)

        t0.start()
        t1.start()
        t2.start()


    def stop(self):
        while len(self.wait_queue):
            continue
        self.contadoresEstatisticos()
        self.isOpen = False

    # Apresenta as metricas
    def contadoresEstatisticos(self):
        print("TempoMedioEspera: %.3f\n"
              "Clientes atendidos: %d\n"
              "TempoMedioServico: %.3f\n"
              "TotalClientesFila: %.3f\n"
              "TempoEsperaBloco1: %.3f\n"
              "TempoEsperaBloco2: %.3f\n"
              "TempoEsperaBloco3: %.3f\n"
              "TempoEsperaBloco4: %.3f" % (myVars.TempoTotalEspera/myVars.CLIENTS_SERVED,
                                           myVars.CLIENTS_SERVED, myVars.TempoTotalServico/myVars.CLIENTS_SERVED,
                                           myVars.TotalClientesFila, myVars.TempoEsperaBloco1,
                                           myVars.TempoEsperaBloco2, myVars.TempoEsperaBloco3,myVars.TempoEsperaBloco4
                                           ))
        outfile = open("resultados.csv","w")
        outfile.write("TempoTotalSistema: %.3f\n"
                      "TempoMedioEspera: %.3f\n"
              "Clientes atendidos: %d\n"
              "TempoMedioServico: %.3f\n"
              "TotalClientesFila: %.3f\n"
              "TempoEsperaBloco1: %.3f\n"
              "TempoEsperaBloco2: %.3f\n"
              "TempoEsperaBloco3: %.3f\n"
              "TempoEsperaBloco4: %.3f" % (myVars.TempoTotalSistema, myVars.TempoTotalEspera/myVars.CLIENTS_SERVED,
                                           myVars.CLIENTS_SERVED, myVars.TempoTotalServico/myVars.CLIENTS_SERVED,
                                           myVars.TotalClientesFila, myVars.TempoEsperaBloco1,
                                           myVars.TempoEsperaBloco2, myVars.TempoEsperaBloco3,myVars.TempoEsperaBloco4
                                           ))
        outfile.close()


    # deve retornar as demais metricas
    def attend(self):
        while self.isOpen:
            if len(self.wait_queue):
                for item in self.wait_queue:
                    client = item[0]
                    clock = item[1]

                    print("Cliente %s chegou no setor %d em %.2f " % (client.token, client.where_am_i, clock.t))

                    if client.where_am_i == 0:
                        self.postos[0].fila_eventos.append(item)

                    elif client.where_am_i == 1:
                        self.postos[1].fila_eventos.append(item)

                    elif client.where_am_i == 2:
                        self.postos[2].fila_eventos.append(item)

                    elif client.where_am_i == -1:
                        self.wait_queue.remove(item)

                myVars.TempoTotalSistema = clock.t

        self.postos[0].stop()
        self.postos[1].stop()
        self.postos[2].stop()

