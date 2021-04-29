#coding: utf-8
import random
import math
import myVars
from myVars import *

def DeterminarTempoEntreChegadas(niu,now):
    r = random.random() / RAND_MAX
    # if now >= 0 and now <= time_block1:
    #     r = 0.45
    # elif now > time_block1 and now <= time_block2:
    #    r = 0.15
    # elif now > time_block2 and now <= time_block3:
    #     r = 0.3
    # elif now > time_block3 and now <= time_block4:
    #     r = 0.1
    X = -niu * math.log(1 - r)
    # X = random.randint(1,5)
    return float(X)

def DeterminarTempoServico(A,B,T0):
    r = random.random()/RAND_MAX
    # r = 0.55
    X = T0 + A + (B - A) * r
    # print("r2 = %f  -- X2 = %f" %( r, X))
    X = random.randint(0, 4000) + T0
    return float(X)



def eventoSaida(c, clock):
    print("Client %s saindo as %.2f" % (c.token, clock.t))
    # print("Tempo saida: %.3f" % clock.t)
    if c.delay > clock.t:
        clock.incr(c.delay)

def eventoChegada(proxima_chegada,clock):
    if proxima_chegada > clock.t:
        # print("clock.t=%.2f -- proxima_chegada=%.2f" % (clock.t, proxima_chegada))
        clock.incr(proxima_chegada)
