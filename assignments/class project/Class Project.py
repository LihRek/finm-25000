'''
The following code was written for a class project for FINM 25000: Quantiative Trading and Portfolio Management
It creates an order management system similar to the ones used by stock exchanges and tests it
'''

import time

from enum import Enum
class OrderType(Enum):
    LIMIT = 1
    MARKET = 2
    IOC = 3
class OrderSide(Enum):
    BUY = 1
    SELL = 2
class NonPositiveQuantity(Exception):
    pass
class NonPositivePrice(Exception):
    pass
class InvalidSide(Exception):
    pass
class UndefinedOrderType(Exception):
    pass
class UndefinedOrderSide(Exception):
    pass
class NewQuantityNotSmaller(Exception):
    pass
class UndefinedTraderAction(Exception):
    pass
class UndefinedResponse(Exception):
    pass
from abc import ABC
class Order(ABC):
    def __init__(self, id, symbol, quantity, side, time):
        self.id = id
        self.symbol = symbol
        if quantity > 0:
            self.quantity = quantity
        else:
            raise NonPositiveQuantity("Quantity Must Be Positive!")
        if side in [OrderSide.BUY, OrderSide.SELL]:
            self.side = side
        else:
            raise InvalidSide("Side Must Be Either \"Buy\" or \"OrderSide.SELL\"!")
        self.time = time
class LimitOrder(Order):
    def __init__(self, id, symbol, quantity, price, side, time):
        super().__init__(id, symbol, quantity, side, time)
        if price > 0:
            self.price = price
        else:
            raise NonPositivePrice("Price Must Be Positive!")
        self.type = OrderType.LIMIT
class MarketOrder(Order):
    def __init__(self, id, symbol, quantity, side, time):
        super().__init__(id, symbol, quantity, side, time)
        self.type = OrderType.MARKET
class IOCOrder(Order):
    def __init__(self, id, symbol, quantity, price, side, time):
        super().__init__(id, symbol, quantity, side, time)
        if price > 0:
            self.price = price
        else:
            raise NonPositivePrice("Price Must Be Positive!")
        self.type = OrderType.IOC
class FilledOrder(Order):
    def __init__(self, id, symbol, quantity, price, side, time, limit = False):
        super().__init__(id, symbol, quantity, side, time)
        self.price = price
        self.limit = limit

from copy import deepcopy

class MatchingEngine():
    def __init__(self):
        self.sum = 0
        self.bid_book = []
        self.ask_book = []

    def handle_order(self, order):
        # this function does not seem to be called by the test cases
        if not isinstance(order.type, OrderType):
            raise UndefinedOrderType("Undefined Order Type!")

        if order.type == OrderType.LIMIT:
            filled = self.handle_limit_order(self, order)
        if order.type == OrderType.MARKET:
            filled = self.handle_market_order(self, order)
        if order.type == OrderType.IOC:
            filled = self.handle_ioc_order(self, order)

    def handle_market_order(self, order):
        filled_orders = []
        if not isinstance(order.side, OrderSide):
            raise UndefinedOrderSide("Undefined Order Side!")

        if order.side == OrderSide.BUY:
            for i in range(len(self.ask_book)):
                if order.quantity == 0:
                    break

                tq = min(self.ask_book[i].quantity, order.quantity)

                filled1 = deepcopy(self.ask_book[i])
                filled1.quantity = tq
                filled2 = deepcopy(order)
                filled2.quantity = tq
                filled2.price = self.ask_book[i].price
                filled_orders.extend([filled1, filled2])

                self.ask_book[i].quantity -= tq
                order.quantity -= tq

            a = [i for i in self.ask_book if i.quantity != 0]
            self.ask_book = a

        if order.side == OrderSide.SELL:
            for i in range(len(self.bid_book)):
                if order.quantity == 0:
                    break

                tq = min(self.bid_book[i].quantity, order.quantity)

                filled1 = deepcopy(self.bid_book[i])
                filled1.quantity = tq
                filled2 = deepcopy(order)
                filled2.quantity = tq
                filled2.price = self.bid_book[i].price
                filled_orders.extend([filled1, filled2])

                self.bid_book[i].quantity -= tq
                order.quantity -= tq

            a = [i for i in self.bid_book if i.quantity != 0]
            self.bid_book = a


        return filled_orders

    def handle_ioc_order(self, order):
        filled_orders = []
        if not isinstance(order.side, OrderSide):
            raise UndefinedOrderSide("Undefined Order Side!")

        if order.side == OrderSide.BUY:
            for i in range(len(self.ask_book)):
                if self.ask_book[i].price > order.price or order.quantity == 0:
                    break

                tq = min(self.ask_book[i].quantity, order.quantity)
                self.sum += tq

                filled1 = deepcopy(self.ask_book[i])
                filled1.quantity = tq
                filled2 = deepcopy(order)
                filled2.quantity = tq
                filled2.price = self.ask_book[i].price
                filled_orders.extend([filled1, filled2])

                self.ask_book[i].quantity -= tq
                order.quantity -= tq

            a = [i for i in self.ask_book if i.quantity != 0]
            self.ask_book = a

        if order.side == OrderSide.SELL:
            for i in range(len(self.bid_book)):
                if self.bid_book[i].price < order.price or order.quantity == 0:
                    break

                tq = min(self.bid_book[i].quantity, order.quantity)
                self.sum += tq

                filled1 = deepcopy(self.bid_book[i])
                filled1.quantity = tq
                filled2 = deepcopy(order)
                filled2.quantity = tq
                filled2.price = self.bid_book[i].price
                filled_orders.extend([filled1, filled2])

                self.bid_book[i].quantity -= tq
                order.quantity -= tq

            a = [i for i in self.bid_book if i.quantity != 0]
            self.bid_book = a

        return filled_orders

    def insert_limit_order(self, order):
        assert order.type == OrderType.LIMIT
        if not isinstance(order.side, OrderSide):
            raise UndefinedOrderSide("Undefined Order Side!")

        if order.side == OrderSide.BUY:
            if len(self.bid_book) == 0:
                self.bid_book.append(order)
                return None
            for i in range(len(self.bid_book)):
                if order.price > self.bid_book[i].price:
                    self.bid_book.insert(i, order)
                    return None
            self.bid_book.append(order)

        if order.side == OrderSide.SELL:
            if len(self.ask_book) == 0:
                self.ask_book.append(order)
                return None
            for i in range(len(self.ask_book)):
                if order.price < self.ask_book[i].price:
                    self.ask_book.insert(i, order)
                    return None
            self.ask_book.append(order)

    def handle_limit_order(self, order):
        self.sum = 0
        filled_orders = []
        if not isinstance(order.side, OrderSide):
            raise UndefinedOrderSide("Undefined Order Side!")

        filled_orders = self.handle_ioc_order(order)
        if order.quantity > 0:
            self.insert_limit_order(order)

        return filled_orders

    def amend_quantity(self, id, quantity):
        for i in range(len(self.bid_book)):
            if self.bid_book[i].id != id:
                continue
            if self.bid_book[i].quantity < quantity:
                raise NewQuantityNotSmaller("Amendment Must Reduce Quantity!")
            self.bid_book[i].quantity = quantity
            return None

        for i in range(len(self.ask_book)):
            if self.ask_book[i].id != id:
                continue
            if self.ask_book[i].quantity < quantity:
                raise NewQuantityNotSmaller("Amendment Must Reduce Quantity!")
            self.ask_book[i].quantity = quantity
            return None
    
    def cancel_order(self, id):
        for i in range(len(self.bid_book)):
            if self.bid_book[i].id == id:
                del self.bid_book[i]
                return None

        for i in range(len(self.ask_book)):
            if self.ask_book[i].id == id:
                del self.ask_book[i]
                return None

import unittest

class TestOrderBook(unittest.TestCase):

    def test_insert_limit_order(self):
        matching_engine = MatchingEngine()
        order = LimitOrder(1, "S", 10, 10, OrderSide.BUY, time.time())
        matching_engine.insert_limit_order(order)

        self.assertEqual(matching_engine.bid_book[0].quantity, 10)
        self.assertEqual(matching_engine.bid_book[0].price, 10)
    
    def test_handle_limit_order(self):
        matching_engine = MatchingEngine()
        order = LimitOrder(1, "S", 10, 10, OrderSide.BUY, time.time())
        matching_engine.insert_limit_order(order)

        order_1 = LimitOrder(2, "S", 5, 10, OrderSide.BUY, time.time())
        order_2 = LimitOrder(3, "S", 10, 15, OrderSide.BUY, time.time())
        matching_engine.handle_limit_order(order_1)
        matching_engine.handle_limit_order(order_2)

        self.assertEqual(matching_engine.bid_book[0].price, 15)
        self.assertEqual(matching_engine.bid_book[1].quantity, 10)

        order_sell = LimitOrder(4, "S", 14, 8, OrderSide.SELL, time.time())
        filled_orders = matching_engine.handle_limit_order(order_sell)

        self.assertEqual(matching_engine.bid_book[0].quantity, 6)
        self.assertEqual(filled_orders[0].id, 3)
        self.assertEqual(filled_orders[0].price, 15)
        self.assertEqual(filled_orders[2].id, 1)
        self.assertEqual(filled_orders[2].price, 10)
    
    def test_handle_market_order(self):
        matching_engine = MatchingEngine()
        order_1 = LimitOrder(1, "S", 6, 10, OrderSide.BUY, time.time())
        order_2 = LimitOrder(2, "S", 5, 10, OrderSide.BUY, time.time())
        matching_engine.handle_limit_order(order_1)
        matching_engine.handle_limit_order(order_2)

        order = MarketOrder(5, "S", 5, OrderSide.SELL, time.time())
        filled_orders = matching_engine.handle_market_order(order)
        self.assertEqual(matching_engine.bid_book[0].quantity, 1)
        self.assertEqual(filled_orders[0].price, 10)

    def test_handle_ioc_order(self):
        matching_engine = MatchingEngine()
        order_1 = LimitOrder(1, "S", 1, 10, OrderSide.BUY, time.time())
        order_2 = LimitOrder(2, "S", 5, 10, OrderSide.BUY, time.time())
        matching_engine.handle_limit_order(order_1)
        matching_engine.handle_limit_order(order_2)

        order = IOCOrder(6, "S", 5, 12, OrderSide.SELL, time.time())
        filled_orders = matching_engine.handle_ioc_order(order)
        self.assertEqual(matching_engine.bid_book[0].quantity, 1)
        self.assertEqual(len(filled_orders), 0)
    
    def test_amend_quantity(self):
        matching_engine = MatchingEngine()
        order_1 = LimitOrder(1, "S", 5, 10, OrderSide.BUY, time.time())
        order_2 = LimitOrder(2, "S", 10, 15, OrderSide.BUY, time.time())
        matching_engine.handle_limit_order(order_1)
        matching_engine.handle_limit_order(order_2)

        matching_engine.amend_quantity(2, 8)
        self.assertEqual(matching_engine.bid_book[0].quantity, 8)
    
    def test_cancel_order(self):
        matching_engine = MatchingEngine()
        order_1 = LimitOrder(1, "S", 5, 10, OrderSide.BUY, time.time())
        order_2 = LimitOrder(2, "S", 10, 15, OrderSide.BUY, time.time())
        matching_engine.handle_limit_order(order_1)
        matching_engine.handle_limit_order(order_2)

        matching_engine.cancel_order(1)
        self.assertEqual(matching_engine.bid_book[0].id, 2)

import io
import __main__
suite = unittest.TestLoader().loadTestsFromModule(__main__)
buf = io.StringIO()
unittest.TextTestRunner(stream=buf, verbosity=2).run(suite)
buf = buf.getvalue().split("\n")
for test in buf:
	if test.startswith("test"):
		print(test)

