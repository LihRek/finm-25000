class OrderManager:
    def __init__(self):
        self.counter = 0
        self.orders = []
        
    def handle_order_from_ts(self,o):
        self.counter += 1
        
        order = o.copy()
        order['state'] = 'new'
        order['id'] = self.counter
        self.orders.append(order)

    def handle_order_from_market(self,o):
        found = False
        for i in range(len(self.orders)):
            if self.orders[i]['id'] != o['id']:
                continue
            found = True
            self.orders[i]['state'] = o['state']
            
        if not found:
            print(f"order id {o['id']} not found")
            
            
    def get_positions(self):
        ans = 0 
        for i in self.orders:
            if i['state'] != 'filled':
                continue
            if i['side'] == 'buy':
                m = 1
            else: 
                m = -1
            ans += i['quantity'] * m
        return ans
        
    def get_holdings(self):
        ans = 0 
        for i in self.orders:
            if i['state'] != 'filled':
                continue
            if i['side'] == 'buy':
                m = 1
            else: 
                m = -1
            ans += i['quantity'] * m * i['price']
        return ans
        
    def get_total_filled(self):
        ans = 0
        for i in self.orders:
            if i['state'] == 'filled':
                ans += 1
        return ans
                
            
    def get_unacknowledged_orders(self):
        ans = 0
        for i in self.orders:
            if i['state'] == 'new':
                ans += 1
        return ans

    def get_unacknowledged_buy_volume(self):
        ans = 0
        for i in self.orders:
            if i['state'] != 'new':
                continue
            if i['side'] != 'buy':
                continue
            ans += i['quantity'] * i['price']      
        return ans

    def get_unacknowledged_sell_volume(self):
        ans = 0
        for i in self.orders:
            if i['state'] != 'new':
                continue
            if i['side'] != 'sell':
                continue
            ans += i['quantity'] * i['price']      
        return ans

def test1():
    om=OrderManager()
    o1={'quantity' : 100, 'price' : 10, 'side' : 'buy'}
    om.handle_order_from_ts(o1)
    print('New order' + str(om.get_unacknowledged_orders()))
    o1['quantity'] = 5
    o1['price']=5
    om.handle_order_from_ts(o1)
    print('New order' + str(om.get_unacknowledged_orders()))
    print('Unacknowledged volume for buy in $:' + str(om.get_unacknowledged_buy_volume()))
    print('Unacknowledged volume for sell in $:' + str(om.get_unacknowledged_sell_volume()))
    o1['side'] = 'sell'
    om.handle_order_from_ts(o1)
    print('Unacknowledged volume for buy in $:' + str(om.get_unacknowledged_buy_volume()))
    print('Unacknowledged volume for sell in $:' + str(om.get_unacknowledged_sell_volume()))
    print('Unacknowledged #:' + str(om.get_unacknowledged_orders()))

    return om

def test2():
    om=test1()
    o1 = {'quantity': 100, 'price': 10, 'side': 'buy' , 'id' : 1 , 'state' : 'filled'}
    om.handle_order_from_market(o1)
    print('Number of fills:' + str(om.get_total_filled()))
    o1['id']=2
    o1['state']='cancelled'
    om.handle_order_from_market(o1)
    print('Number of fills:' + str(om.get_total_filled()))
    print('Unacknowledged #:' + str(om.get_unacknowledged_orders()))
    o1['id'] = 3
    o1['state'] = 'rejected'
    om.handle_order_from_market(o1)
    print('Number of fills:' + str(om.get_total_filled()))
    print('Unacknowledged #:' + str(om.get_unacknowledged_orders()))


def test3():
    om=test1()
    o1 = {'quantity': 100, 'price': 10, 'side': 'buy' , 'id' : 4 , 'state' : 'filled'}
    om.handle_order_from_market(o1)


def test4():
    om=test1()
    o1 = {'quantity': 100, 'price': 10, 'side': 'buy' , 'id' : 1 , 'state' : 'filled'}
    om.handle_order_from_market(o1)
    print('Number of fills:' + str(om.get_total_filled()))
    print('Total position:' + str(om.get_positions()))
    print('Total holdings in $' + str(om.get_holdings()))
    o1['id']=3
    o1['state']='filled'
    om.handle_order_from_market(o1)
    print('Number of fills:' + str(om.get_total_filled()))
    print('Total position:' + str(om.get_positions()))
    print('Total holdings in $' + str(om.get_holdings()))


if __name__ == '__main__':
    test_number = int(input().strip())
    globals()['test'+str(test_number)]()
