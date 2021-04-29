#!/usr/bin/env python2.7
# coding: utf-8
from threading import Thread, ThreadError
from queue import Queue
import time
from functions import *
from servico import Servico
from myVars import *

def determine_clients():
    # priorities
    # -1 - visitantes
    # 0 - geral
    # 1 - retorno
    # 2 - prioritario
    clients_list = list()
    clients_list.append([[0, hex(random.randint(0, 99999)), -1] for i in range(int(visiting_clients))])
    geral_priority = TOTAL_CLIENTS - int(sell_zone_priority_clients + return_zone_clients + visiting_clients)
    clients_list.append([[0, hex(random.randint(0, 99999)), 0] for i in range(int(geral_priority))])
    clients_list.append([[2, hex(random.randint(0, 99999)), 1] for i in range(int(sell_zone_priority_clients))])
    clients_list.append([[1, hex(random.randint(0, 99999)), 2] for i in range(int(return_zone_clients))])

    return clients_list

def existClients(array):
    cont = 0
    for item in array:
        if not len(item):
            cont += 1
    if cont == len(array):
        return False
    return True

class Client():
    def __init__(self, token, priority, T0, destiny,delay=0.0):
        self.token = token
        self.priority = priority
        self.T0 = T0
        self.delay = delay
        self.destiny = destiny
        self.where_am_i = 0

class Clock():
    def __init__(self):
        self.t = 0.0

    def incr(self, value):
        self.t = value

def main():
    # Clients per round
    client_number = 0
    TEMPO = Clock()
    isOpen = True

    # Get awaited clients
    clients_list = determine_clients()
    # do shuffle on the list
    # random.shuffle(clients_list)
    servico = Servico()

    t = Thread(None,servico.attend,None)
    t.start()

    proxima_chegada = 0.000

    while (TEMPO.t <= TEMPO_EXPEDIENTE) and isOpen:
        now = TEMPO.t
        # first block? Apply rules for the first block
        # 10h – 13h → 10%
        if now >= 0 and now <= time_block1:
            client_number = 0.1 * TOTAL_CLIENTS
        elif now > time_block1 and now <= time_block2:
            client_number = 0.3 * TOTAL_CLIENTS
        elif now > time_block2 and now <= time_block3:
            client_number = 0.15 * TOTAL_CLIENTS
        elif now > time_block3 and now <= time_block4:
            client_number = 0.45 * TOTAL_CLIENTS


        for i in range(int(client_number)):
            if existClients(clients_list):
                try:
                    client_class = random.choice(clients_list)
                    chosen_client = client_class[0]
                except Exception as err:
                    # print (clients_list)
                    continue

                proxima_chegada = DeterminarTempoEntreChegadas(2.0, TEMPO.t) + TEMPO.t
                # Atualizar relogio
                eventoChegada(proxima_chegada,TEMPO)

                if not chosen_client: continue

                # chosen_client =  (0,18x1d, 2)

                T0 = proxima_chegada
                token = chosen_client[1]
                priority = chosen_client[0]
                destiny = chosen_client[2]
                c = Client(token, priority, T0, destiny)

                # remove from waiting list
                # clients_list[chosen_client[2]+1].remove(chosen_client)
                del(clients_list[chosen_client[2] + 1][0])

                # Work
                servico.wait_queue.append((c, TEMPO))
                # print("Client just entering in the system at %.2f" % T0)


                myVars.CLIENTS_SERVED+=1
            else:
                isOpen = False
                break

    servico.stop()
    time.sleep(2)
    print("==> ", myVars.CLIENTS_SERVED, TEMPO.t)


if __name__ == '__main__':
    main()