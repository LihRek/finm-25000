#!/bin/python3

import math
import os
import random
import re
import sys
import json
import unittest

class OrderBook:
    def __init__(self):
        self.list_asks = []
        self.list_bids = []
        self.orders = {}
        self.counter = 0
        
    def handle_order(self,o):
        if o['action']=='new':
            self.handle_new(o)
        elif o['action']=='modify':
            self.handle_modify(o)
        elif o['action']=='delete':
            self.handle_delete(o)
        else:
            print('Error-Cannot handle this action')     
            
    def handle_new(self,o):
        self.orders[o['id']] = o
        if o['side'] == 'bid':
            if len(self.list_bids) == 0:
                self.list_bids.append(o)
                return None
            for i in range(len(self.list_bids)):
                if o['price'] > self.list_bids[i]['price']:
                    self.list_bids.insert(i, o)
                    return None
            self.list_bids.append(o)

        if o['side'] == 'ask':
            if len(self.list_asks) == 0:
                self.list_asks.append(o)
                return None
            for i in range(len(self.list_asks)):
                if o['price'] < self.list_asks[i]['price']:
                    self.list_asks.insert(i, o)
                    return None
            self.list_asks.append(o)
            
        

    def handle_modify(self,o):
        for i in range(len(self.list_asks)):
            if self.list_asks[i]['id'] == o['id']:
                self.list_asks[i]['quantity'] = o['quantity']
                break
        for i in range(len(self.list_bids)):
            if self.list_bids[i]['id'] == o['id']:
                self.list_bids[i]['quantity'] = o['quantity']
                break
        self.orders[o['id']]['quantity'] = o['quantity']
                

    def handle_delete(self,o):
        del self.orders[o['id']]
        for i in range(len(self.list_asks)):
            if self.list_asks[i]['id'] == o['id']:
                del self.list_asks[i]
                break
        for i in range(len(self.list_bids)):
            if self.list_bids[i]['id'] == o['id']:
                del self.list_bids[i]
                break

    def find_order_in_a_list(self,o,lookup_list = None):
        pass

    def display_content(self,fptr):
        fptr.write('BIDS\n')
        for o in self.list_bids:
            fptr.write("%d %d %d\n" % (o['id'],o['price'],o['quantity']))
        fptr.write('OFFERS\n')
        for o in self.list_asks:
            fptr.write("%d %d %d\n" % (o['id'],o['price'],o['quantity']))

        
def test_A():
    ob = OrderBook()
    orders = json.loads(input().strip())
    for o in orders:
        ob.handle_new(o)
    if (orders[0]['id'] in ob.orders.keys()) and (orders[0] in ob.list_bids):
        print(f"Implemented handle_new: True")
    else: print(f"Implemented handle_new: False")
    

def test_B():
    ob = OrderBook()
    mod_orderid = None
    orders = json.loads(input().strip())
    while True:
        for order in orders:
            if order['action'] == 'modify':
                ob.handle_modify(order)
                mod_orderid = order['id']
                break
            ob.handle_order(order)
        break
    mod_order = ob.orders.get(mod_orderid, None)
    if (ob.orders[mod_orderid]['quantity'] == 20) and (mod_order in ob.list_bids):
            print(f"Implemented handle_modify: True")
    else: print(f"Implemented handle_modify: False")
    
    
def test_C():
    ob = OrderBook()
    del_orderid = None
    orders = json.loads(input().strip())
    while True:
        for order in orders:
            if order['action'] == 'delete':
                ob.handle_delete(order)
                del_orderid = order['id']
                break
            ob.handle_order(order)
        break
    del_order = ob.orders.get(del_orderid, None)
    if (not del_order) and (del_order not in ob.list_bids):
            print(f"Implemented handle_delete: True")
    else: print(f"Implemented handle_delete: False")
    
    
def test_D():
    fptr = open(os.environ['OUTPUT_PATH'], 'w')

    order_book = OrderBook()

    order_list_from_file = input().strip()

    json_order_list=json.loads(order_list_from_file)
    for order in json_order_list:
        order_book.handle_order(order)
        
    order_book.display_content(fptr)

    fptr.close()


if __name__ == '__main__':
    letter = sys.stdin.readline().strip()
    globals()['test_' + letter]()

    
