__author__ = 'Andrew'

from functools import partial
import random
import pickle
import threading


class Controller_Base():

    def __init__(self):

        self.callbacks = {}

        print('Init Controller base')


    def run(self, function):
        print ("running...")

        t1 = threading.Thread(target=function)
        t1.start()
        #t1.join()

    def subscribeView(self, methods):
        self.callbacks.update(methods)
        pass

    def updateStatus(self, str):
        cb = partial(self.callbacks['statusUpdate'])
        cb(str)

    def updateResult(self, str):
        cb = partial(self.callbacks['resultUpdate'])
        cb(str)

    def pickleDefinitions(self, tree):
        return pickle._dump(tree)

