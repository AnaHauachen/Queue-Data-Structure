from threading import Thread, ThreadError
import sys,os
import time
import random

def insert(array,queue,rightIndex,value):
    i = rightIndex
    while (i >= 0 and queue[array[i]][0] > value):
            array[i+1] = array[i]
            i-=1
    array[i+1] = value

def insertion_sort(queue,array):
    for i in range(1,len(array)):
        insert(array,i-1, queue[array[i]][0])
    return array


class Queue:
    def __init__(self):
        self.memory = dict()
        self.wait_queue = list()
        self.isPriority = False
    def put(self,c):
        try:
            self.memory[c.token] = (c.priority, c)
            if self.isPriority:
                self.wait_queue.append(c.token)
                # Percorre a fila para verificar se
                # o novo cliente tem maior prioridade
                self.wait_queue = insertion_sort(self.memory, self.wait_queue)
                # print (self.wait_queue, self.memory)
            else:
                self.wait_queue.append(c.token)
            return True
        except Exception as err:
            print("Fila",err)
            return False
    def get(self, token):
        return self.memory[token]
    def front(self):
        return self.wait_queue[0]
    def size (self):
        return len(self.memory)
    def getQueue(self):
        return self.memory
    def remove(self,token):
        try:
            del(self.memory[token])
            self.wait_queue.remove(token)
            return True
        except Exception as err:
            print(err)
            return False
