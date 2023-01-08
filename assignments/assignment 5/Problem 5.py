import sys
class OrderNotFoundException(Exception):
    pass
class State:
    ON = 1
    OFF = 2
class OrderState:
    OPEN = 1
    FILLED = 2
    CANCELLED = 3
class OrderSide:
    BUY = 1
    SELL = 2
class AppBase:
    def __init__(self):
        self.state = State.OFF

    def start(self):
        self.state = State.ON

    def stop(self):
        self.state = State.OFF

    def get_state(self):
        return self.state

# You need to build this class
class TradingStrategy(AppBase):
    def __init__(self, name):
        self.name = name
        self.counter = -1
        self.positions = {}
        self.orders = []

    def send_order(self, symbol, price, quantity, side, state=1):
        self.counter += 1
        dictionary = {'strategyname': self.name, 'symbol': symbol, 'price': price, 'quantity': quantity,
                      'order_id': self.counter, 'side': side, 'state': state}
        self.positions[symbol] = 0
        self.orders.append(dictionary)
        return dictionary

    def handle_order_from_market(self, order_execution):
        found = False
        if order_execution['state'] == OrderState.FILLED:
            quantity = order_execution['quantity']
        else:
            quantity = 0
        if order_execution['side'] == OrderSide.BUY:
            m = 1
        else:
            m = -1
        self.positions[order_execution['symbol']] += quantity * m

        for i in range(len(self.orders)):
            if self.orders[i]['order_id'] == order_execution['order_id']:
                del self.orders[i]
                found = True
                break

        if not found:
            raise OrderNotFoundException


class OrderManager(AppBase):
    def __init__(self):
        self.positions = {}
        self.orders = []
        self.eoi = -1

    def handle_order_from_ts(self, order):
        self.eoi += 1
        order['external_order_id'] = self.eoi
        self.orders.append(order)
        try:
            self.positions[order["strategyname"]][order['symbol']] = 0
        except:
            self.positions[order["strategyname"]] = {}
            self.positions[order["strategyname"]][order['symbol']] = 0
        return order

    def handle_order_from_market(self, order_execution):
        found = False
        if order_execution['state'] == OrderState.FILLED:
            quantity = order_execution['quantity']
        else:
            quantity = 0
        if order_execution['side'] == OrderSide.BUY:
            m = 1
        else:
            m = -1
        self.positions[order_execution["strategyname"]][order_execution['symbol']] += quantity * m

        for i in range(len(self.orders)):
            if self.orders[i]['external_order_id'] == order_execution['external_order_id']:
                del self.orders[i]
                found = True
                break
        if not found:
            raise OrderNotFoundException
        return order_execution


class MarkerSimulator(AppBase):
    def __init__(self):
        pass

    def handle_order(self, o):
        if o['external_order_id'] % 2 == 0:
            o['state'] = OrderState.FILLED
        else:
            o['state'] = OrderState.CANCELLED
        return o


def test_base_derived_ts():
    t1 = TradingStrategy('Bob')
    t1.start()
    if t1.get_state() == State.ON: print('SUCCESS')
    t1.stop()
    if t1.get_state() == State.OFF: print('SUCCESS')
    if issubclass(TradingStrategy, AppBase): print('SUCCESS')


def test_base_derived_oms():
    om1 = OrderManager()
    om1.start()
    if om1.get_state() == State.ON: print('SUCCESS')
    om1.stop()
    if om1.get_state() == State.OFF: print('SUCCESS')
    if issubclass(OrderManager, AppBase): print('SUCCESS')


def test_create_new_order():
    t1 = TradingStrategy('Bob')
    order_sent = t1.send_order('MSFT', 15, 100, OrderSide.BUY)
    if (order_sent == {'strategyname': 'Bob', 'symbol': 'MSFT', 'side': 1, 'price': 15, 'quantity': 100, 'order_id': 0,
                       'state': 1}):
        print('SUCCESS')
    else:
        print('FAIL')


def test_create_new_2order():
    t1 = TradingStrategy('Bob')
    order_sent = t1.send_order('MSFT', 15, 100, OrderSide.BUY)
    if (order_sent == {'strategyname': 'Bob', 'symbol': 'MSFT', 'side': 1, 'price': 15, 'quantity': 100, 'order_id': 0,
                       'state': 1}):
        print('SUCCESS')
    else:
        print('FAIL')

    order_sent = t1.send_order('APPL', 45, 250, OrderSide.SELL)
    if (order_sent == {'strategyname': 'Bob', 'symbol': 'APPL', 'side': 2, 'price': 45, 'quantity': 250, 'order_id': 1,
                       'state': 1}):
        print('SUCCESS')
    else:
        print('FAIL')


def test_create_new_2order_from_different_strategy():
    t1 = TradingStrategy('Alice')
    t2 = TradingStrategy('Bob')

    order_sent = t1.send_order('MSFT', 15, 100, OrderSide.BUY)
    if (order_sent == {'strategyname': 'Alice', 'symbol': 'MSFT', 'side': 1, 'price': 15, 'quantity': 100,
                       'order_id': 0, 'state': 1}):
        print('SUCCESS')
    else:
        print('FAIL')

    order_sent = t2.send_order('APPL', 45, 250, OrderSide.SELL)
    if (order_sent == {'strategyname': 'Bob', 'symbol': 'APPL', 'side': 2, 'price': 45, 'quantity': 250, 'order_id': 0,
                       'state': 1}):
        print('SUCCESS')
    else:
        print('FAIL')


def test_strategy_market_response_filled():
    t1 = TradingStrategy('Bob')
    order_sent = t1.send_order('MSFT', 15, 100, OrderSide.BUY)
    if (order_sent == {'strategyname': 'Bob', 'symbol': 'MSFT', 'side': 1, 'price': 15, 'quantity': 100, 'order_id': 0,
                       'state': 1}):
        print('SUCCESS')
    else:
        print('FAIL')
    order_sent['state'] = OrderState.FILLED
    order_received_by_the_trading_strategy = order_sent

    t1.handle_order_from_market(order_received_by_the_trading_strategy)
    if t1.positions == {'MSFT': 100}:
        print('SUCCESS')
    else:
        print('FAIL')


def test_strategy_market_response_cancelled():
    t1 = TradingStrategy('Bob')
    order_sent = t1.send_order('MSFT', 15, 100, OrderSide.BUY)
    if (order_sent == {'strategyname': 'Bob', 'symbol': 'MSFT', 'side': 1, 'price': 15, 'quantity': 100, 'order_id': 0,
                       'state': 1}):
        print('SUCCESS')
    else:
        print('FAIL')
    order_sent['state'] = OrderState.CANCELLED
    order_received_by_the_trading_strategy = order_sent

    t1.handle_order_from_market(order_received_by_the_trading_strategy)
    if t1.positions == {'MSFT': 0}:
        print('SUCCESS')
    else:
        print('FAIL')


def test_strategy_2_filled():
    t1 = TradingStrategy('Bob')
    order_sent = t1.send_order('MSFT', 15, 100, OrderSide.BUY)
    if (order_sent == {'strategyname': 'Bob', 'symbol': 'MSFT', 'side': 1, 'price': 15, 'quantity': 100, 'order_id': 0,
                       'state': 1}):
        print('SUCCESS')
    else:
        print('FAIL')
    order_sent['state'] = OrderState.FILLED
    order_received_by_the_trading_strategy = order_sent

    t1.handle_order_from_market(order_received_by_the_trading_strategy)
    if t1.positions == {'MSFT': 100}:
        print('SUCCESS')
    else:
        print('FAIL')

    order_sent = t1.send_order('AAPL', 15, 50, OrderSide.SELL)
    if (order_sent == {'strategyname': 'Bob', 'symbol': 'AAPL', 'side': 2, 'price': 15, 'quantity': 50, 'order_id': 1,
                       'state': 1}):
        print('SUCCESS')
    else:
        print('FAIL')
    order_sent['state'] = OrderState.FILLED
    order_received_by_the_trading_strategy = order_sent

    t1.handle_order_from_market(order_received_by_the_trading_strategy)
    if t1.positions == {'MSFT': 100, 'AAPL': -50}:
        print('SUCCESS')
    else:
        print('FAIL')


def test_new_order_manager():
    t1 = TradingStrategy('Bob')
    order_sent = t1.send_order('MSFT', 15, 100, OrderSide.BUY)
    om1 = OrderManager()
    om1.handle_order_from_ts(order_sent)
    if om1.positions == {'Bob': {'MSFT': 0}}:
        print('SUCCESS')
    else:
        print('FAIL')


def test_new_order_manager_4_orders():
    t1 = TradingStrategy('Bob')
    t2 = TradingStrategy('Alice')
    order_sent1 = t1.send_order('MSFT', 15, 100, OrderSide.BUY)
    order_sent2 = t1.send_order('AAPL', 15, 120, OrderSide.BUY)
    order_sent3 = t2.send_order('GOOG', 10, 130, OrderSide.SELL)
    order_sent4 = t2.send_order('MSFT', 15, 140, OrderSide.SELL)

    om1 = OrderManager()
    om1.handle_order_from_ts(order_sent1)
    om1.handle_order_from_ts(order_sent2)
    om1.handle_order_from_ts(order_sent3)
    om1.handle_order_from_ts(order_sent4)
    if om1.positions == {'Bob': {'MSFT': 0, 'AAPL': 0}, 'Alice': {'GOOG': 0, 'MSFT': 0}}:
        print('SUCCESS')
    else:
        print('FAIL')


def test_order_manager_market_response():
    t1 = TradingStrategy('Bob')
    order_sent = t1.send_order('MSFT', 15, 100, OrderSide.BUY)
    om1 = OrderManager()
    order_sent = om1.handle_order_from_ts(order_sent)
    order_sent['state'] = OrderState.FILLED
    om1.handle_order_from_market(order_sent)
    if om1.positions == {'Bob': {'MSFT': 100}}:
        print('SUCCESS')
    else:
        print('FAIL')


def test_order_manager_market_4response():
    t1 = TradingStrategy('Bob')
    t2 = TradingStrategy('Alice')
    order_sent1 = t1.send_order('MSFT', 15, 100, OrderSide.BUY)
    order_sent2 = t1.send_order('AAPL', 15, 120, OrderSide.BUY)
    order_sent3 = t2.send_order('GOOG', 10, 130, OrderSide.SELL)
    order_sent4 = t2.send_order('MSFT', 15, 140, OrderSide.SELL)

    om1 = OrderManager()
    order_sent1 = om1.handle_order_from_ts(order_sent1)
    order_sent2 = om1.handle_order_from_ts(order_sent2)
    order_sent3 = om1.handle_order_from_ts(order_sent3)
    order_sent4 = om1.handle_order_from_ts(order_sent4)

    order_sent1['state'] = OrderState.FILLED
    order_sent2['state'] = OrderState.CANCELLED
    order_sent3['state'] = OrderState.CANCELLED
    order_sent4['state'] = OrderState.FILLED

    om1.handle_order_from_market(order_sent1)
    om1.handle_order_from_market(order_sent2)
    om1.handle_order_from_market(order_sent3)
    om1.handle_order_from_market(order_sent4)

    if om1.positions == {'Bob': {'MSFT': 100, 'AAPL': 0}, 'Alice': {'GOOG': 0, 'MSFT': -140}}:
        print('SUCCESS')
    else:
        print('FAIL')


def test_order_manager_list_orders():
    t1 = TradingStrategy('Bob')
    t2 = TradingStrategy('Alice')
    order_sent1 = t1.send_order('MSFT', 15, 100, OrderSide.BUY)
    order_sent2 = t1.send_order('AAPL', 15, 120, OrderSide.BUY)
    order_sent3 = t2.send_order('GOOG', 10, 130, OrderSide.SELL)
    order_sent4 = t2.send_order('MSFT', 15, 140, OrderSide.SELL)

    om1 = OrderManager()
    order_sent1 = om1.handle_order_from_ts(order_sent1)
    order_sent2 = om1.handle_order_from_ts(order_sent2)
    order_sent3 = om1.handle_order_from_ts(order_sent3)
    order_sent4 = om1.handle_order_from_ts(order_sent4)

    if om1.orders == [
        {'strategyname': 'Bob', 'symbol': 'MSFT', 'side': 1, 'price': 15, 'quantity': 100, 'order_id': 0, 'state': 1,
         'external_order_id': 0},
        {'strategyname': 'Bob', 'symbol': 'AAPL', 'side': 1, 'price': 15, 'quantity': 120, 'order_id': 1, 'state': 1,
         'external_order_id': 1},
        {'strategyname': 'Alice', 'symbol': 'GOOG', 'side': 2, 'price': 10, 'quantity': 130, 'order_id': 0, 'state': 1,
         'external_order_id': 2},
        {'strategyname': 'Alice', 'symbol': 'MSFT', 'side': 2, 'price': 15, 'quantity': 140, 'order_id': 1, 'state': 1,
         'external_order_id': 3}]:
        print('SUCCESS')
    else:
        print('FAIL')

    order_sent1['state'] = OrderState.FILLED
    order_sent2['state'] = OrderState.CANCELLED
    order_sent3['state'] = OrderState.CANCELLED
    order_sent4['state'] = OrderState.FILLED

    om1.handle_order_from_market(order_sent1)
    om1.handle_order_from_market(order_sent2)
    om1.handle_order_from_market(order_sent3)
    om1.handle_order_from_market(order_sent4)

    if om1.orders == []:
        print('SUCCESS')
    else:
        print('FAIL')


def test_full_trading_cycle():
    t1 = TradingStrategy('Bob')
    om1 = OrderManager()
    orders_sent = []
    for i in range(10):
        orders_sent.append(t1.send_order('MSFT' if i % 2 == 0 else 'AAPL', 15, i * 100,
                                         OrderSide.BUY if i % 3 == 0 else OrderSide.SELL))
        orders_sent[i] = om1.handle_order_from_ts(orders_sent[i])

    if om1.orders == [
        {'strategyname': 'Bob', 'symbol': 'MSFT', 'side': 1, 'price': 15, 'quantity': 0, 'order_id': 0, 'state': 1,
         'external_order_id': 0},
        {'strategyname': 'Bob', 'symbol': 'AAPL', 'side': 2, 'price': 15, 'quantity': 100, 'order_id': 1, 'state': 1,
         'external_order_id': 1},
        {'strategyname': 'Bob', 'symbol': 'MSFT', 'side': 2, 'price': 15, 'quantity': 200, 'order_id': 2, 'state': 1,
         'external_order_id': 2},
        {'strategyname': 'Bob', 'symbol': 'AAPL', 'side': 1, 'price': 15, 'quantity': 300, 'order_id': 3, 'state': 1,
         'external_order_id': 3},
        {'strategyname': 'Bob', 'symbol': 'MSFT', 'side': 2, 'price': 15, 'quantity': 400, 'order_id': 4, 'state': 1,
         'external_order_id': 4},
        {'strategyname': 'Bob', 'symbol': 'AAPL', 'side': 2, 'price': 15, 'quantity': 500, 'order_id': 5, 'state': 1,
         'external_order_id': 5},
        {'strategyname': 'Bob', 'symbol': 'MSFT', 'side': 1, 'price': 15, 'quantity': 600, 'order_id': 6, 'state': 1,
         'external_order_id': 6},
        {'strategyname': 'Bob', 'symbol': 'AAPL', 'side': 2, 'price': 15, 'quantity': 700, 'order_id': 7, 'state': 1,
         'external_order_id': 7},
        {'strategyname': 'Bob', 'symbol': 'MSFT', 'side': 2, 'price': 15, 'quantity': 800, 'order_id': 8, 'state': 1,
         'external_order_id': 8},
        {'strategyname': 'Bob', 'symbol': 'AAPL', 'side': 1, 'price': 15, 'quantity': 900, 'order_id': 9, 'state': 1,
         'external_order_id': 9}]:
        print('SUCCESS')
    else:
        print('FAIL')

    sim = MarkerSimulator()

    for i in range(10):
        orders_sent[i] = sim.handle_order(orders_sent[i])
        orders_sent[i] = om1.handle_order_from_market(orders_sent[i])
        orders_sent[i] = t1.handle_order_from_market(orders_sent[i])

    if om1.orders == []:
        print('SUCCESS')
    else:
        print('FAIL')

    if om1.positions == {'Bob': {'MSFT': -800, 'AAPL': 0}}:
        print('SUCCESS')
    else:
        print('FAIL')

    if t1.orders == []:
        print('SUCCESS')
    else:
        print('FAIL')

    if t1.positions == {'MSFT': -800, 'AAPL': 0}:
        print('SUCCESS')
    else:
        print('FAIL')
    return om1, t1, sim


def test_full_2_strategies_trading_cycle():
    om1, t1, sim = test_full_trading_cycle()
    t2 = TradingStrategy('Alice')
    orders_sent = []
    for i in range(10):
        orders_sent.append(t2.send_order('MSFT' if i % 2 == 0 else 'AAPL', 15, i * 100,
                                         OrderSide.BUY if i % 3 == 0 else OrderSide.SELL))
        orders_sent[i] = om1.handle_order_from_ts(orders_sent[i])

    if om1.orders == [
        {'strategyname': 'Alice', 'symbol': 'MSFT', 'side': 1, 'price': 15, 'quantity': 0, 'order_id': 0, 'state': 1,
         'external_order_id': 10},
        {'strategyname': 'Alice', 'symbol': 'AAPL', 'side': 2, 'price': 15, 'quantity': 100, 'order_id': 1, 'state': 1,
         'external_order_id': 11},
        {'strategyname': 'Alice', 'symbol': 'MSFT', 'side': 2, 'price': 15, 'quantity': 200, 'order_id': 2, 'state': 1,
         'external_order_id': 12},
        {'strategyname': 'Alice', 'symbol': 'AAPL', 'side': 1, 'price': 15, 'quantity': 300, 'order_id': 3, 'state': 1,
         'external_order_id': 13},
        {'strategyname': 'Alice', 'symbol': 'MSFT', 'side': 2, 'price': 15, 'quantity': 400, 'order_id': 4, 'state': 1,
         'external_order_id': 14},
        {'strategyname': 'Alice', 'symbol': 'AAPL', 'side': 2, 'price': 15, 'quantity': 500, 'order_id': 5, 'state': 1,
         'external_order_id': 15},
        {'strategyname': 'Alice', 'symbol': 'MSFT', 'side': 1, 'price': 15, 'quantity': 600, 'order_id': 6, 'state': 1,
         'external_order_id': 16},
        {'strategyname': 'Alice', 'symbol': 'AAPL', 'side': 2, 'price': 15, 'quantity': 700, 'order_id': 7, 'state': 1,
         'external_order_id': 17},
        {'strategyname': 'Alice', 'symbol': 'MSFT', 'side': 2, 'price': 15, 'quantity': 800, 'order_id': 8, 'state': 1,
         'external_order_id': 18},
        {'strategyname': 'Alice', 'symbol': 'AAPL', 'side': 1, 'price': 15, 'quantity': 900, 'order_id': 9, 'state': 1,
         'external_order_id': 19}]:
        print('SUCCESS')
    else:
        print('FAIL')

    for i in range(10):
        orders_sent[i] = sim.handle_order(orders_sent[i])
        orders_sent[i] = om1.handle_order_from_market(orders_sent[i])
        orders_sent[i] = t2.handle_order_from_market(orders_sent[i])

    if om1.orders == []:
        print('SUCCESS')
    else:
        print('FAIL')

    if om1.positions == {'Bob': {'MSFT': -800, 'AAPL': 0}, 'Alice': {'MSFT': -800, 'AAPL': 0}}:
        print('SUCCESS')
    else:
        print('FAIL')

    if t2.orders == []:
        print('SUCCESS')
    else:
        print('FAIL')

    if t2.positions == {'MSFT': -800, 'AAPL': 0}:
        print('SUCCESS')
    else:
        print('FAIL')


def test_order_manager_market_response_exception():
    t1 = TradingStrategy('Bob')
    order_sent = t1.send_order('MSFT', 15, 100, OrderSide.BUY)
    om1 = OrderManager()
    order_sent = om1.handle_order_from_ts(order_sent)
    order_sent = order_sent.copy()
    order_sent['state'] = OrderState.FILLED
    try:
        order_sent['external_order_id'] = 44
        om1.handle_order_from_market(order_sent)
    except OrderNotFoundException:
        print('SUCCESS')
    except Exception:
        print('FAIL')


def test_order_manager_market_response_2exception():
    t1 = TradingStrategy('Bob')
    order_sent = t1.send_order('MSFT', 15, 100, OrderSide.BUY)
    om1 = OrderManager()
    order_sent = om1.handle_order_from_ts(order_sent)
    order_sent = order_sent.copy()
    order_sent['state'] = OrderState.FILLED
    try:
        order_sent['external_order_id'] = 44
        om1.handle_order_from_market(order_sent)
    except OrderNotFoundException:
        print('SUCCESS')
    except Exception:
        print('FAIL')
    try:
        order_sent['order_id'] = 44
        t1.handle_order_from_market(order_sent)
    except OrderNotFoundException:
        print('SUCCESS')
    except Exception:
        print('FAIL')


if __name__ == '__main__':
    func_name = sys.stdin.readline().strip()
    test_func = globals()[func_name]
    test_func()
