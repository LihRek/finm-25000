class Side:
    BUY = 1
    SELL = 2


class TradeManager(Side):
    def __init__(self,bal=1000):
        self.balance = bal
        self.positions = {}
        self.trades = []
        self.pnls = {}
    def __repr__(self):
        return f'Balance:{self.balance}\n{self.ans}\n{self.pnl}'

    def handle_transaction(self, trade):
        if trade['side'] == 1:
            m = -1
        else:
            m = 1
        self.balance += trade['quantity']*trade['price']*m
        try:
            self.positions[trade['symbol']] += trade['quantity'] * m
        except:
            self.positions[trade['symbol']] = trade['quantity'] * m
        ans = 'Positions:'
        for i in self.positions:
            ans += str(i) + ' ' + str(self.positions[i]) + ','
        self.ans = ans[0:-1]
        
        try:
            self.pnls[trade['symbol']] += trade['quantity'] * m * trade['price']
        except:
            self.pnls[trade['symbol']] = trade['quantity'] * m * trade ['price']
        ans2 = 'PNLs:'
        for i in self.pnls:
            ans2 += str(i) + ' ' + str(self.pnls[i]) + ','
        self.pnl = ans2[0:-1]
    
    def set_balance(self,bal):
        if bal < 0:
            print('Negative Balance Not Accepted')
        self.balance = bal
    
    def update_balance(self, trade):
        if trade['side']== 1:
            self.balance = self.balance - (trade['quantity']*trade['price'])
        elif trade['side']==2:
            self.balance = self.balance + (trade['quantity']*trade['price'])

    def update_position(self,trade):
        if trade['side'] == 1:
            m = 1
        else:
            m = -1
        try:
            self.positions[trade['symbol']] += trade['quantity'] * m
        except:
            self.positions[trade['symbol']] = trade['quantity'] * m
      
    def update_pnl(self, trade):
        if trade['side'] == 1:
            m = -1
        else:
            m = 1
        try:
            self.pnls[trade['symbol']] += trade['quantity'] * m * trade['price']
        except:
            self.pnls[trade['symbol']] = trade['quantity'] * m * trade ['price']
    
    def repr_position(self):
        ans = 'Positions:'
        for i in self.positions:
            ans += str(i) + ' ' + str(self.positions[i]) + ','
        return ans[0:-1]
    
    def repr_pnl(self):
        pnls = 'PNLs:'
        for i in self.pnls:
            pnls += str(i) + ' ' + str(self.pnls[i]) + ','
        return pnls[0:-1]
    
    def repr_balance(self):
        result = f'Balance:{self.balance}'
        return result

def test_position_1():
    tm1=TradeManager(100000)
    t1={'quantity' : 100, 'price' : 1.2, 'side' : Side.BUY, 'symbol' : 'EUR/USD'}
    t2={'quantity' : 100, 'price' : 1.3, 'side' : Side.SELL, 'symbol' : 'USD/CAD'}
    tm1.update_position(t1)
    tm1.update_position(t2)
    print(tm1.repr_position())

def test_position_2():
    tm1=TradeManager(100000)
    t1={'quantity' : 100, 'price' : 1.2, 'side' : Side.BUY, 'symbol' : 'EUR/USD'}
    t2={'quantity' : 100, 'price' : 1.3, 'side' : Side.SELL, 'symbol' : 'EUR/USD'}
    tm1.update_position(t1)
    tm1.update_position(t2)
    print(tm1.repr_position())

def test_pnl_1():
    tm1=TradeManager(100000)
    t1={'quantity' : 100, 'price' : 1.2, 'side' : Side.BUY, 'symbol' : 'EUR/USD'}
    t2={'quantity' : 100, 'price' : 1.3, 'side' : Side.SELL, 'symbol' : 'EUR/USD'}
    tm1.update_pnl(t1)
    tm1.update_pnl(t2)
    print(tm1.repr_pnl())

def test_pnl_2():
    tm1=TradeManager(100000)
    t1={'quantity' : 100, 'price' : 1.2, 'side' : Side.BUY, 'symbol' : 'EUR/USD'}
    tm1.update_pnl(t1)
    print(tm1.repr_pnl())

def test_balance_1():
    tm1=TradeManager(100000)
    t1={'quantity' : 100, 'price' : 1.2, 'side' : Side.BUY, 'symbol' : 'EUR/USD'}
    tm1.update_balance(t1)
    print(tm1.repr_balance())

def test_balance_2():
    tm1=TradeManager(100000)
    t1={'quantity' : 100, 'price' : 1.2, 'side' : Side.BUY, 'symbol' : 'EUR/USD'}
    t2={'quantity' : 100, 'price' : 1.3, 'side' : Side.SELL, 'symbol' : 'EUR/USD'}
    tm1.update_balance(t1)
    tm1.update_balance(t2)
    print(tm1.repr_balance())

def test_balance_3():
    tm1=TradeManager()
    t1={'quantity' : 100, 'price' : 1.2, 'side' : Side.BUY, 'symbol' : 'EUR/USD'}
    tm1.update_balance(t1)
    print(tm1.repr_balance())


def test_transaction_1():
    tm1=TradeManager(100000)
    t1={'quantity' : 100, 'price' : 1.2, 'side' : Side.BUY, 'symbol' : 'EUR/USD'}
    t2={'quantity' : 100, 'price' : 1.3, 'side' : Side.SELL, 'symbol' : 'EUR/USD'}
    tm1.handle_transaction(t1)
    tm1.handle_transaction(t2)
    print(tm1)

def test_transaction_2():
    tm1=TradeManager(100000)
    t1={'quantity' : 100, 'price' : 1.2, 'side' : Side.BUY, 'symbol' : 'EUR/USD'}
    t2={'quantity' : 100, 'price' : 1.3, 'side' : Side.SELL, 'symbol' : 'EUR/USD'}
    t3 = {'quantity': 1000, 'price': 1.1, 'side': Side.BUY, 'symbol': 'USD/CAD'}
    t4 = {'quantity': 1000, 'price': 1.4, 'side': Side.SELL, 'symbol': 'USD/CAD'}

    tm1.handle_transaction(t1)
    tm1.handle_transaction(t2)
    tm1.handle_transaction(t3)
    tm1.handle_transaction(t4)

    print(tm1)

def test_balance_4():
    tm1=TradeManager()
    t1={'quantity' : 100, 'price' : 1.2, 'side' : Side.BUY, 'symbol' : 'EUR/USD'}
    tm1.update_balance(t1)
    tm1.set_balance(123)
    print(tm1.repr_balance())
    try:
        tm1.set_balance(-123)
    except NegativeBalanceError as e:
        print(e)


if __name__ == '__main__':
    func_name = input().strip()
    globals()[func_name]()
